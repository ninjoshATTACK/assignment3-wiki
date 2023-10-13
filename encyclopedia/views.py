from django.shortcuts import render
from django import forms
from markdown2 import Markdown
import random

from . import util
import encyclopedia

# Lets me use Markdown
markdowner = Markdown()

# Class used for entries and search
class SearchForm(forms.Form):
    query = forms.CharField(max_length=100)

# Class for creating new entries
class CreateForm(forms.Form):
    title = forms.CharField(label="Add Title")
    body = forms.CharField(label="Add Body", widget=forms.Textarea())

class EditForm(forms.Form):
    title = forms.CharField(label="Edit Title")
    body = forms.CharField(label="Edit Body", widget=forms.Textarea())

# Home Page
def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

# Entry Page
def entry(request, title):
    e = util.get_entry(title)
    if e is None:
        form = SearchForm()
        content = "The entry you are trying to access does not exist."
        return render(request, "encyclopedia/error.html", {
            "form": form, "content": content
        })
    else:
        form = SearchForm()
        mdfile = util.get_entry(title)
        # Convert md to html
        htmlfile = markdowner.convert(mdfile)
        return render(request, "encyclopedia/entry.html", {
            "title": title, "content": htmlfile, "form": form
        })

# Search
def search(request):
    if request.method == "GET":
        q = request.GET.get("q","")

        if q != "":
            showentry = False
            for entry in util.list_entries():
                # Search result was found
                if q.lower() == entry.lower():
                    mdfile = util.get_entry(q)
                    htmlfile = markdowner.convert(mdfile)
                    showentry = True
                    break
            # Display entry if found
            if showentry:
                return render(request, "encyclopedia/entry.html", {
                    "title": entry, "content": htmlfile, "form": q
                })
            else:
                results = []
                for entry in util.list_entries():
                    # To see if substring is found in entries
                    if q.lower() in entry.lower():
                        results.append(entry)
                # Substring was not found in all the entries
                if len(results) == 0:
                    form = SearchForm()
                    content = "The page you searched for does not exist."
                    return render(request, "encyclopedia/error.html", {
                        'form': form, "content": content
                    })
                # The substring was found in these entries
                else:
                    return render(request, "encyclopedia/search.html", {
                        "entries": results, "form": q
                    })
    else:
        form = SearchForm()
        content = "No search result was found."
        return render(request, "encyclopedia/error.html", {
            'form': form, 'content': content
        })

# Create a New Entry Page
def create(request):
    if request.method == "POST":
        createform = CreateForm(request.POST)
        if createform.is_valid():
            title = createform.cleaned_data.get("title")
            body = createform.cleaned_data.get("body")
            exists = False
            # See if title is already taken
            for entry in util.list_entries():
                if title.lower() == entry.lower():
                    exists = True
                    break
            # Title is already in entries
            if exists:
                content = "This page already exists."
                form = SearchForm()
                return render(request, "encyclopedia/error.html", {
                    'form': form, "content": content
                })
            # Title doesn't exist so save the entry
            else:
                util.save_entry(title, body)
                form = SearchForm()
                mdfile = util.get_entry(title)
                htmlfile = markdowner.convert(mdfile)
                return render(request, "encyclopedia/entry.html", {
                    "title": title, "content": htmlfile, "form": form
                })
    else:
        form = SearchForm()
        createform = CreateForm()
        return render(request, "encyclopedia/create.html", {
            "form": form, "createform": createform
        })

# Edit Page
def edit(request, title):
    if request.method == "POST":
        editform = EditForm(request.POST)
        if editform.is_valid():
            title = editform.cleaned_data.get("title")
            body = editform.cleaned_data.get("body")
            util.save_entry(title, body)
            form = SearchForm()
            htmlfile = markdowner.convert(body)
            return render(request, "encyclopedia/entry.html", {
                "title": title, "content": htmlfile, "form": form
            })
    else:
        form = SearchForm()
        editform = EditForm({"title": title, "body": util.get_entry(title)})
        return render(request, "encyclopedia/edit.html", {
            "form": form, "editform": editform
        })

# Random Page
def randomEntry(request):
    entries = util.list_entries()
    length = len(entries)
    chosen = random.randint(0, length-1)
    title = entries[chosen]
    mdfile = util.get_entry(title)
    htmlfile = markdowner.convert(mdfile)
    form = SearchForm()
    return render(request, "encyclopedia/entry.html", {
        "title": title, "content": htmlfile, "form": form
    })
