import os
import requests
import json
import time

CACHE_FILE = os.path.join(os.path.dirname(__file__), "../resources/cache/crypto_cache.json")
CACHE_TTL = 3 * 24 * 60 * 60  # cache for 3 days

def load_cache():
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, "r") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return {}
    return {}

def save_cache(cache):
    os.makedirs(os.path.dirname(CACHE_FILE), exist_ok=True)
    with open(CACHE_FILE, "w") as f:
        json.dump(cache, f)

def get_watched_cryptos():
    cache = load_cache()
    return cache.get("watched_cryptos", ["bitcoin", "ethereum", "dogecoin"])

def save_watched_cryptos(cryptos):
    cache = load_cache()
    cache["watched_cryptos"] = cryptos
    save_cache(cache)

def get_crypto_data(ids=None, vs_currency="usd", force_refresh=False):
    if ids is None:
        ids = get_watched_cryptos()
    cache = load_cache()
    now = time.time()
    prices = cache.get("prices", {})

    # Check cache for all ids
    all_cached = True
    for id_ in ids:
        if (id_ not in prices or (now - prices[id_]["timestamp"] > CACHE_TTL)):
            all_cached = False
            break

    if all_cached and not force_refresh:
        return {id_: prices[id_] for id_ in ids}

    # Fetch from CoinGecko
    ids_str = ",".join(ids)
    url = "https://api.coingecko.com/api/v3/coins/markets"
    params = {
        "vs_currency": vs_currency,
        "ids": ids_str,
        "order": "market_cap_desc",
        "per_page": len(ids),
        "page": 1,
        "sparkline": "false"
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()

        # Update cache
        for coin in data:
            prices[coin["id"]] = {
                "price": coin["current_price"],
                "icon": coin["image"],
                "name": coin["name"],
                "symbol": coin["symbol"].upper(),
                "timestamp": now
            }
        cache["prices"] = prices
        save_cache(cache)

        return {coin["id"]: prices[coin["id"]] for coin in data}
    except Exception as e:
        print(f"Error fetching crypto data: {e}")
        # fallback to cached data if any
        return {id_: prices.get(id_, None) for id_ in ids}