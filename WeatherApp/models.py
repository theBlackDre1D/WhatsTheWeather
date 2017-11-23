from django.db import models

class Forecast(models.Model):
    temperature = models.IntegerField()
    description = models.CharField(max_length = 128)
    pressure = models.IntegerField()
    wind = models.IntegerField()

    def __str__(self):
        return temperature + '/n' + description + '/n' + pressure + '/n' + wind
