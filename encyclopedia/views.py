from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django import forms
from markdown2 import Markdown
import os
from . import util
import random


class new_wiki_form(forms.Form):
    title = forms.CharField(label="Title", required=True)
    content = forms.CharField(label="Content", required=True, widget=forms.Textarea(attrs={
        'id': 'exampleFormControlTextarea1', 'class': "form-control form-control-sm", 'row': "1"}))


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def get_wiki(request, name):
    class edit_wiki_form(forms.Form):
        entry_content = forms.CharField(
            label="Content", required=True, initial=util.get_entry(name), widget=forms.Textarea(attrs={'id': 'exampleFormControlTextarea1', 'class': "form-control form-control-lg", 'row': "3"}))
    entry = None
    if request.method == "POST":
        form = edit_wiki_form(request.POST)
        if form.is_valid():
            entry = form.cleaned_data["entry_content"]
            util.save_entry(name, entry)
    # Get entry|| Assign string not found any
    else:
        entry = "This entry doesn't exist." if util.get_entry(
            name) is None else util.get_entry(name)
    markdowner = Markdown()
    entry = markdowner.convert(entry)
    return render(request, "encyclopedia/get_wiki.html", {
        "entry": entry,
        "name": name
    })


def search_results(request):
    result = request.POST['q']
    if util.get_entry(result) is not None:
        print(result)
        return HttpResponseRedirect(f'wiki/{result}')

    search_entries = []
    for entry in util.list_entries():
        entry = entry.lower()
        result.lower()
        try:
            if entry.index(result) >= 0:
                search_entries.append(entry.capitalize())
        except ValueError:
            print(entry)
    return render(request, "encyclopedia/search_results.html", {
        "entries": search_entries
    })


def random_page(request):
    entries = util.list_entries()
    entry = entries[random.randint(0, len(entries) - 1)]
    return HttpResponseRedirect(f'wiki/{entry}')


def add_page(request):

    return render(request, "encyclopedia/new_wiki.html", {
        "form": new_wiki_form()
    })


def check_new_entry(request):

    if request.method == "POST":
        # take the data from post
        form = new_wiki_form(request.POST)

        # Check if the form is valid (server-side)
        if form.is_valid():
            # Isolate the variables from the 'cleaned version'
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            added_title = util.add_entry(title, content)
        if not added_title:
            print("It already exists")
            return HttpResponse('<h1>Error: The entry already exists</h1> <a href="/add_page" > Go back </a>')

        return HttpResponseRedirect(f'wiki/{title}')

    return HttpResponse("Error! Please revisit the website")


def edit_entry(request, name):
    class edit_wiki_form(forms.Form):
        entry_content = forms.CharField(
            label="Content", required=True, initial=util.get_entry(name), widget=forms.Textarea(attrs={'id': 'exampleFormControlTextarea1', 'class': "form-control form-control-lg", 'row': "3"}))
    return render(request, "encyclopedia/edit_entry.html", {
        "entry_name": name,
        "form": edit_wiki_form()
    })
