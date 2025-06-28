import unittest
from unittest.mock import patch, MagicMock
from weather_info import get_location_coords, get_onecall_weather, get_dashboard_data

class TestWeatherInfo(unittest.TestCase):
    @patch('weather_info.requests.get')
    def test_get_location_coords_success(self, mock_get):
        mock_get.return_value = MagicMock(status_code=200)
        mock_get.return_value.json.return_value = [{
            'lat': 37.5665, 'lon': 126.9780
        }]
        coords = get_location_coords('서울')
        self.assertEqual(coords, (37.5665, 126.9780))

    @patch('weather_info.requests.get')
    def test_get_location_coords_fail(self, mock_get):
        mock_get.return_value = MagicMock(status_code=200)
        mock_get.return_value.json.return_value = []
        coords = get_location_coords('없는도시')
        self.assertIsNone(coords)

    @patch('weather_info.requests.get')
    def test_get_onecall_weather_success(self, mock_get):
        mock_get.return_value = MagicMock(status_code=200)
        mock_get.return_value.json.return_value = {'current': {'temp': 20}}
        data = get_onecall_weather(37.5665, 126.9780)
        self.assertIn('current', data)
        self.assertEqual(data['current']['temp'], 20)

    @patch('weather_info.get_onecall_weather')
    @patch('weather_info.get_location_coords')
    def test_get_dashboard_data(self, mock_coords, mock_onecall):
        mock_coords.return_value = (37.5665, 126.9780)
        mock_onecall.return_value = {
            'current': {
                'temp': 21, 'feels_like': 20, 'weather': [{'description': '맑음'}],
                'rain': {'1h': 0}, 'wind_speed': 2, 'humidity': 50, 'pressure': 1012
            },
            'daily': [
                {'dt': 1719000000, 'temp': {'day': 22}, 'weather': [{'description': '맑음'}], 'rain': 0, 'wind_speed': 2}
            ]
        }
        dashboard = get_dashboard_data(['서울'])
        self.assertEqual(dashboard[0]['name'], '서울')
        self.assertEqual(dashboard[0]['current']['temp'], 21)
        self.assertEqual(dashboard[0]['forecast'][0]['temp'], 22)

if __name__ == '__main__':
    unittest.main()
