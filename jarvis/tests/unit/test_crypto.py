import unittest
from unittest.mock import patch, MagicMock
import time
from jarvis.modules.crypto import (
    get_crypto_data,
    get_watched_cryptos,
    save_watched_cryptos,
)

class TestCrypto(unittest.TestCase):

    @patch("jarvis.modules.crypto.load_cache")
    def test_get_watched_cryptos_default(self, mock_load_cache):
        mock_load_cache.return_value = {}
        result = get_watched_cryptos()
        self.assertEqual(result, ["bitcoin", "ethereum", "dogecoin"])

    @patch("jarvis.modules.crypto.save_cache")
    @patch("jarvis.modules.crypto.load_cache")
    def test_save_watched_cryptos(self, mock_load_cache, mock_save_cache):
        mock_load_cache.return_value = {}
        cryptos = ["bitcoin", "cardano"]
        save_watched_cryptos(cryptos)
        mock_save_cache.assert_called_once()
        args, kwargs = mock_save_cache.call_args
        self.assertEqual(args[0]["watched_cryptos"], cryptos)

    @patch("jarvis.modules.crypto.requests.get")
    @patch("jarvis.modules.crypto.load_cache")
    @patch("jarvis.modules.crypto.save_cache")
    def test_get_crypto_data_api_success(self, mock_save_cache, mock_load_cache, mock_requests_get):
        mock_load_cache.return_value = {}

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = [
            {
                "id": "bitcoin",
                "current_price": 60000,
                "image": "https://example.com/bitcoin.png",
                "name": "Bitcoin",
                "symbol": "btc",
            }
        ]
        mock_requests_get.return_value = mock_response

        with patch("jarvis.modules.crypto.time.time", return_value=1000000):
            result = get_crypto_data(ids=["bitcoin"], force_refresh=True)

        self.assertIn("bitcoin", result)
        self.assertEqual(result["bitcoin"]["price"], 60000)
        self.assertEqual(result["bitcoin"]["symbol"], "BTC")

    @patch("jarvis.modules.crypto.load_cache")
    def test_get_crypto_data_from_cache(self, mock_load_cache):
        now = time.time()
        mock_load_cache.return_value = {
            "prices": {
                "bitcoin": {
                    "price": 50000,
                    "icon": "https://example.com/bitcoin.png",
                    "name": "Bitcoin",
                    "symbol": "BTC",
                    "timestamp": now
                }
            }
        }

        with patch("jarvis.modules.crypto.time.time", return_value=now):
            result = get_crypto_data(ids=["bitcoin"], force_refresh=False)

        self.assertIn("bitcoin", result)
        self.assertEqual(result["bitcoin"]["price"], 50000)

    @patch("jarvis.modules.crypto.requests.get")
    @patch("jarvis.modules.crypto.load_cache")
    def test_get_crypto_data_api_failure(self, mock_load_cache, mock_requests_get):
        now = time.time()
        mock_load_cache.return_value = {
            "prices": {
                "bitcoin": {
                    "price": 50000,
                    "icon": "https://example.com/bitcoin.png",
                    "name": "Bitcoin",
                    "symbol": "BTC",
                    "timestamp": now
                }
            }
        }

        mock_requests_get.side_effect = Exception("API failure")

        with patch("jarvis.modules.crypto.time.time", return_value=now):
            result = get_crypto_data(ids=["bitcoin"], force_refresh=True)

        self.assertEqual(result["bitcoin"]["price"], 50000)  # Fallback to cache on error

if __name__ == "__main__":
    unittest.main()
