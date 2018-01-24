import json

import requests
from django.shortcuts import render
from geopy.geocoders import Nominatim
from forecastiopy import *
from datetime import date, timedelta

from . import forms, models


def index(request):
    city_form = forms.SearchForm()
    DarkSkyAPIKey = '65a79529abb596fddb1eca28b2d1dd8a'
    found_city = ''
    # respond = None
    # api_key = '02e9a702a6f14213bc9125617170112'
    # client = ApixuClient(api_key)
    day_count = '8'

    if request.method == "POST":

        city_form = forms.SearchForm(request.POST)
        if city_form.is_valid():
            found_city = city_form.cleaned_data['cityName']
            print("Printing user input")
            print("Input from user: " + city_form.cleaned_data['cityName'])
            # dict_for_show = {'city': city_form}
            API_response_current = requests.get(
                'http://api.openweathermap.org/data/2.5/weather?q=' + found_city +
                '&units=metric&APPID=86b95a6bdcdc3337e011d61ce6f359a3')

            # Finding latitude and longitude
            geolocator = Nominatim()
            location = geolocator.geocode(found_city)
            print((location.latitude, location.longitude))

            DESIRED_LOCATION = [location.latitude, location.longitude]
            # forecast = ForecastIO.ForecastIO(DarkSkyAPIKey,
            #                                  units=ForecastIO.ForecastIO.UNITS_AUTO,
            #                                  lang=ForecastIO.ForecastIO.LANG_ENGLISH,
            #                                  latitude=DESIRED_LOCATION[0], longitude=DESIRED_LOCATION[1])
            # if forecast.has_hourly() is True:
            #     hourly = ForecastIO.ForecastIO(forecast)
            #     print('Hourly')
            #     print('Summary:', hourly.summary)
            #     print('Icon:', hourly.icon)
            #
            #     for hourForecast in range(0, 23):
            #         print("Daco sa spravilo")

            API_response_days = requests.get('https://api.darksky.net/forecast/' + DarkSkyAPIKey + '/' + str(location.latitude) + ',' + str(location.longitude) + '?units=si')
            if API_response_current.status_code == 200:  # APIREsponse.ok()
                # respond = API_response_current.text
                #print(API_response_current.json())
                respondJSON = json.loads(API_response_current.text)
                description = respondJSON['weather'][0]['main']
                temperature = respondJSON['main']['temp']
                pressure = respondJSON['main']['pressure']
                wind = respondJSON['wind']['speed']
                forecast_dict = {'description': description, 'temperature': temperature, 'pressure': pressure, 'wind': wind, 'city': city_form}

                if API_response_days.status_code == 200:
                    respond_days_JSON = json.loads(API_response_days.text)
                    print(respond_days_JSON)

                    # ---7-DAYS FORECAST---
                    weekday = date.today()
                    for index in range(0, 7):
                        day_in_week = date.strftime(weekday, '%a')
                        day_tempMAX = respond_days_JSON['daily']['data'][index]['temperatureHigh']
                        day_tempMIN = respond_days_JSON['daily']['data'][index]['temperatureLow']
                        day_clouds = respond_days_JSON['daily']['data'][index]['cloudCover']
                        forecast_dict['day_MAX{}'.format(index)] = day_tempMAX
                        forecast_dict['day_MIN{}'.format(index)] = day_tempMIN
                        forecast_dict['day_clouds{}'.format(index)] = day_clouds
                        forecast_dict['day_name{}'.format(index)] = day_in_week
                        weekday += timedelta(days=1)

                    # ---HOURLY---
                    for index in range(0, 24):
                        hour_temp = respond_days_JSON['hourly']['data'][index]['temperature']
                        hour_clouds = respond_days_JSON['hourly']['data'][index]['cloudCover']
                        hour_wind_speed = respond_days_JSON['hourly']['data'][index]['windSpeed']
                        forecast_dict['hour_temp{}'.format(index)] = hour_temp
                        forecast_dict['hour_clouds{}'.format(index)] = hour_clouds
                        forecast_dict['hour_wind_speed{}'.format(index)] = hour_wind_speed




                return render(request, 'WeatherApp/index.html', forecast_dict)

            else:
                print("We do not have weather information for that location :( )")
                return render(request, 'WeatherApp/index.html', {
                    'error': 'We could not find weather information for your location.', 'city': city_form})


    # if (respond != None):
    #     print(respond)
    if request.method == "GET":
        # forecastList = Forecast.objects.all()
        # forecast_dict = {'forecast':forecastList}
        dict_for_show = {'city': city_form}
        return render(request, 'WeatherApp/index.html', dict_for_show)
