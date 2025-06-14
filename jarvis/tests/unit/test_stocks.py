import unittest
from unittest.mock import patch, mock_open, MagicMock
import json
import time
from jarvis.modules.stocks import get_stock_price, get_watched_stocks, save_watched_stocks, CACHE_TTL

class TestStocks(unittest.TestCase):

    @patch("jarvis.modules.stocks.load_cache")
    def test_get_watched_stocks(self, mock_load_cache):
        mock_load_cache.return_value = {"watched_stocks": ["AAPL", "GOOGL"]}
        result = get_watched_stocks()
        self.assertEqual(result, ["AAPL", "GOOGL"])

    @patch("jarvis.modules.stocks.save_cache")
    @patch("jarvis.modules.stocks.load_cache")
    def test_save_watched_stocks(self, mock_load_cache, mock_save_cache):
        mock_load_cache.return_value = {}
        save_watched_stocks(["AAPL", "TSLA"])
        mock_save_cache.assert_called_once()
        args, kwargs = mock_save_cache.call_args
        self.assertEqual(args[0]["watched_stocks"], ["AAPL", "TSLA"])

    @patch("jarvis.modules.stocks.requests.get")
    @patch("jarvis.modules.stocks.load_cache")
    @patch("jarvis.modules.stocks.save_cache")
    def test_get_stock_price_api_call(self, mock_save_cache, mock_load_cache, mock_requests_get):
        # No cache or expired cache → should hit API
        mock_load_cache.return_value = {}

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"c": 150.0}
        mock_requests_get.return_value = mock_response

        with patch("jarvis.modules.stocks.time.time", return_value=1000000):
            price = get_stock_price(symbol="AAPL", force_refresh=True)

        self.assertEqual(price, 150.0)
        mock_requests_get.assert_called_once()

    @patch("jarvis.modules.stocks.load_cache")
    def test_get_stock_price_from_cache(self, mock_load_cache):
        # Cached result within TTL → should NOT hit API
        now = time.time()
        mock_load_cache.return_value = {
            "prices": {
                "AAPL": {
                    "price": 145.0,
                    "timestamp": now
                }
            }
        }

        with patch("jarvis.modules.stocks.time.time", return_value=now):
            price = get_stock_price(symbol="AAPL", force_refresh=False)

        self.assertEqual(price, 145.0)

    @patch("jarvis.modules.stocks.requests.get")
    @patch("jarvis.modules.stocks.load_cache")
    def test_get_stock_price_api_error(self, mock_load_cache, mock_requests_get):
        mock_load_cache.return_value = {}

        mock_response = MagicMock()
        mock_response.status_code = 500
        mock_requests_get.return_value = mock_response

        price = get_stock_price(symbol="AAPL", force_refresh=True)
        self.assertEqual(price, "No Data")

    @patch("jarvis.modules.stocks.requests.get")
    @patch("jarvis.modules.stocks.load_cache")
    def test_get_stock_price_no_price(self, mock_load_cache, mock_requests_get):
        mock_load_cache.return_value = {}

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"c": "N/A"}
        mock_requests_get.return_value = mock_response

        price = get_stock_price(symbol="AAPL", force_refresh=True)
        self.assertEqual(price, "N/A")

if __name__ == "__main__":
    unittest.main()