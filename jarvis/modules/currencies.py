import requests
import os
import json
import time

CACHE_FILE = os.path.join(os.path.dirname(__file__), "../resources/cache/currency_cache.json")
CACHE_TTL = 3 * 24 * 60 * 60  # 3 days in seconds

def load_cache():
    if not os.path.exists(CACHE_FILE):
        return {}
    try:
        with open(CACHE_FILE, "r") as f:
            return json.load(f)
    except Exception:
        return {}

def save_cache(data):
    os.makedirs(os.path.dirname(CACHE_FILE), exist_ok=True)
    with open(CACHE_FILE, "w") as f:
        json.dump(data, f)

def get_rates(base="PLN", symbols=None):
    symbols_str = ",".join(symbols) if symbols else ""
    cache = load_cache()

    now = time.time()
    cache_key = f"{base}:{symbols_str}"

    if cache_key in cache:
        cached_time = cache[cache_key].get("timestamp", 0)
        if now - cached_time < CACHE_TTL:
            return cache[cache_key]["rates"], None  # use cached

    url = f"https://api.frankfurter.app/latest?from={base}&to={symbols_str}"
    try:
        response = requests.get(url)
        if response.status_code == 404:
            return {}, f"Incorrect currency code: '{base}' or '{symbols_str}'"
        response.raise_for_status()
        data = response.json()
        rates = data.get("rates", {})
        cache[cache_key] = {
            "timestamp": now,
            "rates": rates
        }
        save_cache(cache)
        return rates, None
    except requests.exceptions.RequestException as e:
        if cache_key in cache:
            return cache[cache_key]["rates"], f"Error fetching fresh data, using cache: {e}"
        return {}, str(e)

def get_available_currencies():
    url = "https://api.frankfurter.app/currencies"
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json(), None
    except requests.RequestException as e:
        return {}, str(e)