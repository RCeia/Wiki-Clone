from django import forms
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages
from . import util
from markdown2 import Markdown

class SearchForm(forms.Form):
    # Form Class For Search Bar
    search = forms.CharField(label="", widget=forms.TextInput(attrs={
      "class": "search",
      "placeholder": "Search Zikipedia"}))

class NewForm(forms.Form):
    # Form Class for New Entries
    title = forms.CharField(label="", widget=forms.TextInput(attrs={
      "placeholder": "Entry Title"}))
    text = forms.CharField(label="", widget=forms.Textarea(attrs={
        "placeholder": "Enter Entry Content (You Can Use GitHub Markdown))"
    }))

def index(request):
    #Retrun Basic Index Page
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
    #Get Form
    if request.method == "POST":
        form = SearchForm(request.POST)
        #Check If Form is valid
        if form.is_valid():
            title = form.cleaned_data["search"]
            entries = util.get_entry(title)
            #Return Exact Search
            if entries:
                return redirect(reverse("entry", args=[title]))
            #Return Search Results
            else:
                related = util.related(title)

                return render(request, "encyclopedia/search.html", {
                "related": related,
                "title": title,
                "search_form": SearchForm(),
                })

def new(request):
    # New Zikipedia Entry
    # Handles Basic GET Request
    if request.method == "GET":
        return render(request, "encyclopedia/new.html", {
          "new_form": NewForm(),
          "search_form": SearchForm(),
        })
    # Handles POST Request
    elif request.method == "POST":
        form = NewForm(request.POST)

        # Form Process and Validation
        if form.is_valid():
          title = form.cleaned_data["title"]
          text = form.cleaned_data["text"]
        else:
          messages.error(request, "Form is not Valid, Try Doing it Again!")
        # Check If Entry Already Exists 
        if util.get_entry(title):
            messages.error(request, "The Entry You Are Trying To Create Already Exists, You Can Edit It Instead!")
        # If not, Create a new one!
        else:
            util.save_entry(title, text),
            messages.success(request, f'New Entry "{title}" Has Been Submited!')
        return render(request, "encyclopedia/new.html", {
          "new_form": form,
          "search_form": SearchForm(),
        })
    

def edit(request, title):
  
  return render(request, "encyclopedia/edit.html", {
  "title": title,
  "search_form": SearchForm(),
  })