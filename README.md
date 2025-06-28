# Korea City Weather Dashboard

This project is a Python Flask web application that visualizes the current weather and 7-day forecast for all metropolitan and special cities in South Korea using the OpenWeatherMap API.

## Features
- Dark theme dashboard with sidebar tab UI (Home/Report)
- Interactive map (Leaflet) with weather markers for all major Korean cities
- Click a city marker to view detailed weather and 7-day forecast below the map
- Report tab: select a city from a dropdown and view a full weather report (all available info)
- Uses OpenWeather One Call 3.0 API (paid plan required)
- Includes unit test code

## Quick Start
1. Install Python 3.x and pip
2. Install dependencies:
   ```
   pip install flask requests
   ```
3. Copy `.weather_api_key.example` to `.weather_api_key` and put your OpenWeatherMap API key in `.weather_api_key` (key only, one line)
4. Run the server:
   ```
   python3 weather_info.py
   ```
5. Open your browser at `http://localhost:5050/dashboard`

## Project Structure
- `weather_info.py` : Main Flask app (all dashboard/map/report logic)
- `templates/dark_tab_dashboard.html` : Main dashboard UI (all other templates are removed)
- `test_weather_info.py` : Unit tests
- `.weather_api_key` : Your OpenWeatherMap API key (not committed)
- `.weather_api_key.example` : Example API key file

## API Key Setup

1. Copy `.weather_api_key.example` to `.weather_api_key` in the project root.
2. Put your actual OpenWeatherMap API key in `.weather_api_key` (one line, no quotes).
3. **Never commit your real API key to GitHub!**

.gitignore already prevents accidental upload of your API key file.

## Run Unit Tests

To run the included unit tests:

```
python3 -m unittest test_weather_info.py
```

## Notes
- One Call 3.0 API requires a paid plan. Free API keys only support `/data/2.5/weather` and `/data/2.5/forecast` endpoints.
- The only dashboard UI is the dark tab dashboard at `/dashboard`.
- You can easily add or remove cities in the code.

## License
MIT
