import json

import requests
from django.shortcuts import render

from . import forms, models


def index(request):
    city_form = forms.SearchForm()
    found_city = ''
    respond = None

    if request.method == "POST":
        city_form = forms.SearchForm(request.POST)
        if city_form.is_valid():
            found_city = city_form.cleaned_data['cityName']
            print("Printing user input")
            print("Input from user: " + city_form.cleaned_data['cityName'])
            # dict_for_show = {'city': city_form}
            API_response = requests.get(
                'http://api.openweathermap.org/data/2.5/weather?q=' + found_city + '&units=metric&APPID=86b95a6bdcdc3337e011d61ce6f359a3')
            if API_response.status_code == 200:  # APIREsponse.ok()
                # respond = API_response.text
                print(API_response.json())
                respondJSON = json.loads(API_response.text)
                description = respondJSON['weather'][0]['main']
                temperature = respondJSON['main']['temp']
                pressure = respondJSON['main']['pressure']
                wind = respondJSON['wind']['speed']
                forecast_dict = {'description':description,'temperature':temperature,'pressure':pressure,'wind':wind,'city': city_form}
                return render(request, 'WeatherApp/index.html', forecast_dict)
                # cityForecast = Forecast.objects.get_or_create(description=description, tempreature=tempreature,
                #                                               pressure=pressure,
                #                                               wind=wind)  # Now I zhould jave it in database
            else:
                print("We do not have weather information for that location :( )")
                return render(request,'WeatherApp/index.html',{'error':'We could not find weather information for your location.','city': city_form})

    # if (respond != None):
    #     print(respond)
    if request.method == "GET":
        # forecastList = Forecast.objects.all()
        # forecast_dict = {'forecast':forecastList}
        dict_for_show = {'city': city_form}
        return render(request, 'WeatherApp/index.html', dict_for_show)
