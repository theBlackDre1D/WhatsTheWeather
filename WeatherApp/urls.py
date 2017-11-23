from django.conf.urls import url
from WeatherApp import views

urlpatterns = [
    url(r'^$',views.index,name = 'index'),
    url(r'^$',views.forecast,name = 'result')
]
