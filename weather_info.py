from flask import Flask, render_template, jsonify, request
import requests
from datetime import datetime, timedelta
import os

app = Flask(__name__)

# OpenWeatherMap API 사용 (무료 가입 필요, 실제 서비스 시 API 키를 환경변수 등으로 분리 권장)

def load_api_key():
    key_path = os.path.join(os.path.dirname(__file__), '.weather_api_key')
    try:
        with open(key_path, 'r') as f:
            return f.read().strip()
    except Exception:
        return None

API_KEY = load_api_key()
GEOCODE_URL = 'http://api.openweathermap.org/geo/1.0/direct'
WEATHER_URL = 'https://api.openweathermap.org/data/2.5/weather'
FORECAST_URL = 'https://api.openweathermap.org/data/2.5/forecast'
ONECALL_URL = 'https://api.openweathermap.org/data/3.0/onecall'


def get_location_coords(region_name):
    if not API_KEY:
        print('API key is missing.')
        return None
    # Only city/metropolitan level is supported, not district/county. Try both Korean and English.
    candidates = [region_name, region_name.replace('시', ''), region_name.replace('구', ''), region_name.replace('군', '')]
    eng_map = {
        '서울': 'Seoul', '부산': 'Busan', '대구': 'Daegu', '광주': 'Gwangju',
        '인천': 'Incheon', '대전': 'Daejeon', '울산': 'Ulsan', '제주': 'Jeju',
        '수원': 'Suwon', '안양': 'Anyang', '창원': 'Changwon', '고양': 'Goyang',
        '용인': 'Yongin', '성남': 'Seongnam', '청주': 'Cheongju', '천안': 'Cheonan',
        '전주': 'Jeonju', '포항': 'Pohang', '김해': 'Gimhae', '평택': 'Pyeongtaek',
        '의정부': 'Uijeongbu', '시흥': 'Siheung', '파주': 'Paju', '구미': 'Gumi',
        '남양주': 'Namyangju', '김포': 'Gimpo', '원주': 'Wonju', '아산': 'Asan',
        '익산': 'Iksan', '경산': 'Gyeongsan', '거제': 'Geoje', '양산': 'Yangsan',
        '제천': 'Jecheon', '홍성': 'Hongseong', '춘천': 'Chuncheon', '강릉': 'Gangneung',
        '목포': 'Mokpo', '여수': 'Yeosu', '순천': 'Suncheon', '군산': 'Gunsan',
        '광명': 'Gwangmyeong', '평창': 'Pyeongchang', '속초': 'Sokcho', '삼척': 'Samcheok',
        '동해': 'Donghae', '태백': 'Taebaek', '정선': 'Jeongseon', '철원': 'Cheorwon',
        '화천': 'Hwacheon', '양구': 'Yanggu', '인제': 'Inje', '고성': 'Goseong',
        '양양': 'Yangyang', '홍천': 'Hongcheon', '횡성': 'Hoengseong', '영월': 'Yeongwol',
    }
    # Try both Korean and English candidates
    for cand in candidates:
        for q in [cand, eng_map.get(cand, None)]:
            if not q:
                continue
            params = {
                'q': q + ',KR',
                'limit': 1,
                'appid': API_KEY
            }
            try:
                print(f"Geocode request: {params['q']}")
                resp = requests.get(GEOCODE_URL, params=params)
                print(f"Geocode response code: {resp.status_code}")
                print(f"Geocode response: {resp.text[:200]}")
                resp.raise_for_status()
                data = resp.json()
                if data and isinstance(data, list):
                    print(f"Coordinates result: {data[0]['lat']}, {data[0]['lon']}")
                    return data[0]['lat'], data[0]['lon']
            except Exception as e:
                print(f"Geocode error: {e}")
                continue
    print(f"No coordinates found: {region_name}")
    return None


def get_current_weather(lat, lon):
    if not API_KEY:
        return None
    params = {
        'lat': lat,
        'lon': lon,
        'appid': API_KEY,
        'units': 'metric',
        'lang': 'kr'
    }
    try:
        resp = requests.get(WEATHER_URL, params=params)
        resp.raise_for_status()
        return resp.json()
    except Exception:
        return None


def get_weekly_forecast(lat, lon):
    if not API_KEY:
        return None
    params = {
        'lat': lat,
        'lon': lon,
        'appid': API_KEY,
        'units': 'metric',
        'lang': 'kr'
    }
    try:
        resp = requests.get(FORECAST_URL, params=params)
        resp.raise_for_status()
        return resp.json()
    except Exception:
        return None


def get_onecall_weather(lat, lon):
    if not API_KEY:
        return None
    params = {
        'lat': lat,
        'lon': lon,
        'appid': API_KEY,
        'units': 'metric',
        'lang': 'kr'
    }
    try:
        resp = requests.get(ONECALL_URL, params=params)
        resp.raise_for_status()
        return resp.json()
    except Exception as e:
        print(f"OneCall API error: {e}")
        return None

def get_dashboard_data(city_list):
    dashboard = []
    for city in city_list:
        entry = {'name': city, 'error': None, 'current': None, 'forecast': []}
        coords = get_location_coords(city)
        if not coords:
            entry['error'] = 'Could not find location.'
            dashboard.append(entry)
            continue
        lat, lon = coords
        onecall = get_onecall_weather(lat, lon)
        if not onecall or 'current' not in onecall:
            entry['error'] = 'Could not fetch weather data.'
            dashboard.append(entry)
            continue
        c = onecall['current']
        entry['current'] = {
            'temp': c.get('temp'),
            'feels_like': c.get('feels_like'),
            'weather': c.get('weather', [{}])[0].get('description', ''),
            'rain': c.get('rain', {}).get('1h', 0),
            'wind': c.get('wind_speed'),
            'humidity': c.get('humidity'),
            'pressure': c.get('pressure')
        }
        # Up to 7 days daily forecast
        if 'daily' in onecall:
            for d in onecall['daily'][:7]:
                entry['forecast'].append({
                    'date': datetime.fromtimestamp(d['dt']).strftime('%Y-%m-%d'),
                    'temp': d['temp']['day'],
                    'weather': d['weather'][0]['description'],
                    'rain': d.get('rain', 0),
                    'wind': d['wind_speed']
                })
        dashboard.append(entry)
    return dashboard


@app.route('/dashboard/')
@app.route('/dashboard')
def dashboard_view():
    return render_template('dark_tab_dashboard.html')


# Remove or comment out other dashboard routes if not needed

# List of major metropolitan/special cities to display on the map (example)
MAJOR_CITIES = [
    '서울', '부산', '대구', '인천', '광주', '대전', '울산', '세종',
    '수원', '용인', '고양', '창원', '성남', '부천', '화성', '남양주',
    '전주', '천안', '안산', '안양'
]

@app.route('/dashboard/map_data')
def map_data():
    """
    Returns the name, latitude, and longitude of each city to be displayed on the map (used as markers in the frontend)
    """
    result = []
    for city in MAJOR_CITIES:
        coords = get_location_coords(city)
        if coords:
            lat, lon = coords
            result.append({'name': city, 'lat': lat, 'lon': lon})
    return jsonify(result)

@app.route('/dashboard/city_weather')
def city_weather():
    """
    Receives a city name and returns current + 7-day forecast using the One Call 3.0 API (for map/report)
    """
    city = request.args.get('name')
    if not city:
        return jsonify({'error': 'No city specified.'})
    coords = get_location_coords(city)
    if not coords:
        return jsonify({'error': 'Could not find location.'})
    lat, lon = coords
    onecall = get_onecall_weather(lat, lon)
    if not onecall or 'current' not in onecall:
        return jsonify({'error': 'Could not fetch weather data.'})
    c = onecall['current']
    result = {
        'name': city,
        'current': {
            'temp': c.get('temp'),
            'feels_like': c.get('feels_like'),
            'weather': c.get('weather', [{}])[0].get('description', ''),
            'rain': c.get('rain', {}).get('1h', 0),
            'wind': c.get('wind_speed'),
            'humidity': c.get('humidity'),
            'pressure': c.get('pressure')
        },
        'forecast': []
    }
    if 'daily' in onecall:
        for d in onecall['daily'][:7]:
            result['forecast'].append({
                'date': datetime.fromtimestamp(d['dt']).strftime('%Y-%m-%d'),
                'temp': d['temp']['day'],
                'weather': d['weather'][0]['description'],
                'rain': d.get('rain', 0),
                'wind': d['wind_speed']
            })
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5050)
