import json

import requests
from django.shortcuts import render

from . import forms, models


def index(request):
    cityForm = forms.SearchForm()
    foundCity = ''
    respond = None

    if request.method == "POST":
        cityForm = forms.SearchForm(request.POST)
        if cityForm.is_valid():
            foundCity = cityForm.cleaned_data['cityName']
            print("Printing user input")
            print("Input from user: " + cityForm.cleaned_data['cityName'])
            dict_for_show = {'city': cityForm}
            APIResponse = requests.get(
                'http://api.openweathermap.org/data/2.5/weather?q=' + foundCity + '&units=metric&APPID=86b95a6bdcdc3337e011d61ce6f359a3')
            if (APIResponse.status_code == 200):  # APIREsponse.ok()
                # respond = APIResponse.text
                print(APIResponse.json())
                respondJSON = json.loads(APIResponse.text)
                description = respondJSON['weather'][0]['main']
                temperature = respondJSON['main']['temp']
                pressure = respondJSON['main']['pressure']
                wind = respondJSON['wind']['speed']
                forecastDict = {}
                return render(request, 'WeatherApp/index.html', {'description': description, 'city': cityForm})
                cityForecast = Forecast.objects.get_or_create(description=description, tempreature=tempreature,
                                                              pressure=pressure,
                                                              wind=wind)  # Now I zhould jave it in database
            else:
                print("We do not have weather information for that location :( )")

    # if (respond != None):
    #     print(respond)
    if request.method == "GET":
        # forecastList = Forecast.objects.all()
        # forecastDict = {'forecast':forecastList}
        dict_for_show = {'city': cityForm}
        return render(request, 'WeatherApp/index.html', dict_for_show)


def forecast(request):
    dictForShow = {'context': context}
    return (request, 'WeatherApp/skuska.html', dictForShow)
