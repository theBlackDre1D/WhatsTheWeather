import json

import requests
from django.shortcuts import render
from apixu.client import ApixuClient, ApixuException

from . import forms, models

def index(request):
    city_form = forms.SearchForm()
    found_city = ''
    respond = None
    api_key = '02e9a702a6f14213bc9125617170112'
    client = ApixuClient(api_key)
    day_count = '7'

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

            API_response_days = requests.get('http://api.apixu.com/v1/forecast.json?key=02e9a702a6f14213bc9125617170112&q=' + found_city + '&days=' + day_count)
            if API_response_current.status_code == 200:  # APIREsponse.ok()
                # respond = API_response_current.text
                print(API_response_current.json())
                respondJSON = json.loads(API_response_current.text)
                description = respondJSON['weather'][0]['main']
                temperature = respondJSON['main']['temp']
                pressure = respondJSON['main']['pressure']
                wind = respondJSON['wind']['speed']
                forecast_dict = {'description': description, 'temperature': temperature, 'pressure': pressure, 'wind': wind, 'city': city_form}

                if API_response_days.status_code == 200:
                    print(API_response_days.json())
                    respond_days_JSON = json.loads(API_response_days.text)
                    #TODO: Check if value in for loop is correct with final count of days for show
                    for index in range(int(day_count)): #There is value of count days for forecast
                        day_temp = respond_days_JSON['forecast']['forecastday'][index]['day']['avgtemp_c']
                        forecast_dict['day{}'.format(index)] = day_temp

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
