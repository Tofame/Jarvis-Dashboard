import os
import requests
import json
import time

CACHE_FILE = os.path.join(os.path.dirname(__file__), "../resources/cache/stocks_cache.json")
CACHE_TTL = 3 * 24 * 60 * 60  # 3 days

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

def get_watched_stocks():
    cache = load_cache()
    return cache.get("watched_stocks", [])

def save_watched_stocks(stocks):
    cache = load_cache()
    cache["watched_stocks"] = stocks
    save_cache(cache)

def get_stock_price(symbol="AAPL", force_refresh=False):
    cache = load_cache()
    now = time.time()

    prices = cache.get("prices", {})

    if (not force_refresh and
        symbol in prices and
        now - prices[symbol]["timestamp"] < CACHE_TTL):
        return prices[symbol]["price"]

    api_key = os.getenv("FINNHUB_API_KEY")
    url = f"https://finnhub.io/api/v1/quote?symbol={symbol}&token={api_key}"
    response = requests.get(url)

    if response.status_code != 200:
        return "No Data"

    data = response.json()
    price = data.get("c", "N/A")
    if price == "N/A":
        return price

    # Update prices cache
    prices[symbol] = {
        "price": price,
        "timestamp": now
    }

    cache["prices"] = prices
    save_cache(cache)

    return price