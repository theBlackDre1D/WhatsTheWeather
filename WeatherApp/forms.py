from django import forms

class SearchForm(forms.Form):
    cityName = forms.CharField(label="City")