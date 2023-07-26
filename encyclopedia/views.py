from django.shortcuts import render
from django import forms
from . import util

class SearchForm(forms.Form):
    # Form Class For Search Bar
    search = forms.CharField(label='', widget=forms.TextInput(attrs={
      "class": "search",
      "placeholder": "Search Zikipedia"}))

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "search_form": SearchForm(),
    })

