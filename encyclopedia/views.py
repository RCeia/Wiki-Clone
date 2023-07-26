from django.shortcuts import render, redirect
from django.urls import reverse
from django import forms
from . import util
from markdown2 import Markdown

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

def entry(request, title):
    #Display Entry Pages

    entries = util.get_entry(title)

    if entries != None:
        #If it exists, Display
        entry = Markdown().convert(entries)
        return render(request, "encyclopedia/entry.html", {
          "title": title,
          "entry": entry,
          "search_form": SearchForm(),
          })
    else:
        # If not, Display Error
        return render(request, "encyclopedia/error.html", {
          "title": title,
          "search_form": SearchForm(),
          })
    
def search(request):
    if request.method == "POST":
        form = SearchForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["search"]
            entries = util.get_entry(title)
            if entries:
                return redirect(reverse('entry', args=[title]))
    return render(request, "encyclopedia/search.html", {
        "title": title,
        "search_form": SearchForm(),
          })

