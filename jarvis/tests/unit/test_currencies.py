import unittest
from unittest.mock import patch, MagicMock
import time

import requests

from jarvis.modules.currencies import get_rates, get_available_currencies, load_cache, save_cache, CACHE_TTL


class TestCurrency(unittest.TestCase):

    @patch("jarvis.modules.currencies.load_cache")
    @patch("jarvis.modules.currencies.save_cache")
    @patch("jarvis.modules.currencies.requests.get")
    def test_get_rates_cache_hit(self, mock_requests_get, mock_save_cache, mock_load_cache):
        now = time.time()
        mock_load_cache.return_value = {
            "PLN:USD": {
                "timestamp": now,
                "rates": {"USD": 0.25}
            }
        }

        rates, error = get_rates(base="PLN", symbols=["USD"])
        self.assertIsNone(error)
        self.assertEqual(rates, {"USD": 0.25})
        mock_requests_get.assert_not_called()

    @patch("jarvis.modules.currencies.load_cache")
    @patch("jarvis.modules.currencies.save_cache")
    @patch("jarvis.modules.currencies.requests.get")
    def test_get_rates_api_success(self, mock_requests_get, mock_save_cache, mock_load_cache):
        mock_load_cache.return_value = {}

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "rates": {"USD": 0.25}
        }
        mock_requests_get.return_value = mock_response

        with patch("jarvis.modules.currencies.time.time", return_value=1000000):
            rates, error = get_rates(base="PLN", symbols=["USD"])

        self.assertIsNone(error)
        self.assertEqual(rates, {"USD": 0.25})
        mock_save_cache.assert_called_once()

    @patch("jarvis.modules.currencies.load_cache")
    @patch("jarvis.modules.currencies.requests.get")
    def test_get_rates_api_404(self, mock_requests_get, mock_load_cache):
        mock_load_cache.return_value = {}

        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_requests_get.return_value = mock_response

        rates, error = get_rates(base="INVALID", symbols=["USD"])
        self.assertEqual(rates, {})
        self.assertTrue("Incorrect currency code" in error)

    @patch("jarvis.modules.currencies.load_cache")
    @patch("jarvis.modules.currencies.requests.get")
    def test_get_rates_api_failure_with_cache(self, mock_requests_get, mock_load_cache):
        stale_timestamp = time.time() - (CACHE_TTL + 10)  # stale cache

        mock_load_cache.return_value = {
            "PLN:USD": {
                "timestamp": stale_timestamp,
                "rates": {"USD": 0.3}
            }
        }

        mock_requests_get.side_effect = requests.exceptions.RequestException("API down")

        rates, error = get_rates(base="PLN", symbols=["USD"])
        self.assertEqual(rates, {"USD": 0.3})
        self.assertTrue("using cache" in error)

    @patch("jarvis.modules.currencies.requests.get")
    def test_get_available_currencies_success(self, mock_requests_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"USD": "United States Dollar", "PLN": "Polish Zloty"}
        mock_requests_get.return_value = mock_response

        result, error = get_available_currencies()
        self.assertIsNone(error)
        self.assertIn("USD", result)
        self.assertIn("PLN", result)

    @patch("jarvis.modules.currencies.requests.get")
    def test_get_available_currencies_failure(self, mock_requests_get):
        mock_requests_get.side_effect = requests.RequestException("Connection error")

        result, error = get_available_currencies()
        self.assertEqual(result, {})
        self.assertIn("Connection error", error)

if __name__ == "__main__":
    unittest.main()