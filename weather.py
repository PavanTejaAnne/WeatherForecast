import datetime
import json
import urllib.request
from pyowm import OWM
from itertools import islice
 # import requests
# send_url = 'http://freegeoip.net/json'
# r = requests.get(send_url)
# j = json.loads(r.text)
# lat = j['latitude']
# lon = j['longitude']

user_api = '1f06c99f1678cc081eff475a29df81da'
unit = 'metric'

adversities = ['sunny','hazy', 'rain', 'windy', 'raining', 'hot', 'snowing','snow','hail', 'hailing',
           'rainy','snowy', 'drizzle', 'drizzling', 'cold']

forecast = ['tomorrow', 'week']

def time_converter(time):
    converted_time = datetime.datetime.fromtimestamp(
        int(time)
    ).strftime('%I:%M %p')
    return converted_time


def url(city_name):
    full_api_url = 'http://api.openweathermap.org/data/2.5/weather?q=' + str(city_name) +\
                   '&mode=json&units=' + unit + '&APPID=' + user_api
    return full_api_url


def data_collection(full_api_url):
    with urllib.request.urlopen(full_api_url) as url:
        return json.loads(url.read().decode('utf-8'))


def data_organizer(raw_data):
    # print(raw_data)
    main = raw_data.get('main')
    sys = raw_data.get('sys')
    data = dict(
        city=raw_data.get('name'),
        country=sys.get('country'),
        temp=main.get('temp'),
        temp_max=main.get('temp_max'),
        temp_min=main.get('temp_min'),
        humidity=main.get('humidity'),
        pressure=main.get('pressure'),
        sky=raw_data['weather'][0]['main'],
        sunrise=time_converter(sys.get('sunrise')),
        sunset=time_converter(sys.get('sunset')),
        wind=raw_data.get('wind').get('speed'),
        wind_deg=raw_data.get('deg'),
        dt=time_converter(raw_data.get('dt')),
        cloudiness=raw_data.get('clouds').get('all')
    )
    return data


def output(data):

    data['m_symbol'] = '\xb0' + 'C'
    s = '''---------------------------------------
Current weather in: {city}, {country}:
{temp}{m_symbol} {sky}
Max: {temp_max}, Min: {temp_min}

Wind Speed: {wind}, Degree: {wind_deg}
Humidity: {humidity}
Cloud: {cloudiness}
Pressure: {pressure}
Sunrise at: {sunrise}
Sunset at: {sunset}

Last Called: {dt}
---------------------------------------'''
    print(s.format(**data))

if __name__ == '__main__':

    API_key = '1f06c99f1678cc081eff475a29df81da'
    owm = OWM(API_key)
    owm.get_API_key()

    try:
        ip = input('Enter your query:').split(" ")

        obs = owm.weather_at_place(str(ip))
        obs.get_reception_time(timeformat='iso')
        w = obs.get_weather()
        l = obs.get_location()

        today_forecast_3hrs = owm.three_hours_forecast(str(ip))
        tf3 = today_forecast_3hrs.get_forecast()

        tomorrow_forecast = owm.daily_forecast(str(ip))
        tf = tomorrow_forecast.get_forecast()

        weekly_forecast = owm.daily_forecast(str(ip))
        wf = weekly_forecast.get_forecast()

        if 'tomorrow' in ip:
            for condition in islice(tf, 1, 2):
                print('yolo')
                print('''-----------------
Date/Time: {}  
Weather Status: {} ({})
Cloud Coverage: {}
Rain: {}
Wind Speed: {[speed]}
Morning Temperature: {[day]}\xb0C
Night Temperature: {[night]}\xb0C
Min Temperature: {[min]}\xb0C
Max Temperature: {[max]}\xb0C
----------------------------
             '''
                      .format(condition.get_reference_time('iso'), condition.get_status(),
                              condition.get_detailed_status(), condition.get_clouds(), condition.get_rain(),
                              condition.get_wind(), condition.get_temperature(unit='celsius'),
                              condition.get_temperature(unit='celsius'), condition.get_temperature(unit='celsius'),
                              condition.get_temperature(unit='celsius')
                              ))

        elif 'today' in ip:
            for condition in islice(tf3, 0, 3):
                print('mama')
                print('''Date/Time: {} 
Weather Status: {} ({})
Cloud Coverage: {}
Rain: {}
Wind Speed: {[speed]}
Temperature: {[temp]}\xb0C

                      '''
                      .format(condition.get_reference_time('iso'), condition.get_status(),
                              condition.get_detailed_status(), condition.get_clouds(), condition.get_rain(),
                              condition.get_wind(), condition.get_temperature(unit='celsius'),
                              ))

        elif 'week' in ip:
            for condition in wf:
                print('hola')
                print('''-----------------
Date/Time: {}  
Weather Status: {} ({})
Cloud Coverage: {}
Rain: {}
Wind Speed: {[speed]}
Morning Temperature: {[day]}\xb0C
Night Temperature: {[night]}\xb0C
Min Temperature: {[min]}\xb0C
Max Temperature: {[max]}\xb0C
----------------------------
                             '''
                      .format(condition.get_reference_time('iso'), condition.get_status(),
                              condition.get_detailed_status(), condition.get_clouds(), condition.get_rain(),
                              condition.get_wind(), condition.get_temperature(unit='celsius'),
                              condition.get_temperature(unit='celsius'), condition.get_temperature(unit='celsius'),
                              condition.get_temperature(unit='celsius')
                              ))

        else:
            output(data_organizer(data_collection(url(ip))))

    except IOError:
        print('Some error buddy boy')
