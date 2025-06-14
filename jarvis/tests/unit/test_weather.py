import unittest
from unittest.mock import patch
from jarvis.modules.weather import get_weather

class TestWeather(unittest.TestCase):
    @patch('jarvis.modules.weather.requests.get')
    def test_get_weather_valid_city(self, mock_get):
        mock_response = unittest.mock.Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'current': {
                'temp_c': 20.5,
                'condition': {
                    'text': 'Sunny',
                    'icon': '//cdn.weatherapi.com/weather/64x64/day/113.png'
                }
            }
        }
        mock_get.return_value = mock_response

        result, error = get_weather("Warsaw")
        self.assertIsNone(error)
        temp_c, condition, icon_url = result
        self.assertEqual(temp_c, 20.5)
        self.assertEqual(condition, 'Sunny')
        self.assertTrue(icon_url.startswith('https://'))

    @patch('jarvis.modules.weather.requests.get')
    def test_get_weather_invalid_city(self, mock_get):
        mock_response = unittest.mock.Mock()
        mock_response.status_code = 401
        mock_get.return_value = mock_response

        result, error = get_weather("InvalidCity")
        self.assertIsNone(result)
        self.assertTrue("API Error" in error)

if __name__ == "__main__":
    unittest.main()