from django.shortcuts import render
from django import forms
from markdown2 import Markdown
import random

from . import util
import encyclopedia

# Lets me use Markdown
markdowner = Markdown()

# Class for entries
class SearchForm(forms.Form):
    query = forms.CharField(max_length=100)

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

# Search NOT WORKING YET
def search(request):
    if request.method == "POST":
        form = SearchForm(request.POST)
        if form.is_valid():
            input = form.cleaned_data.get("query")
            showentry = False
            for entry in util.list_entries():
                # Search result was found
                if input == entry:
                    mdfile = util.get_entry()
                    htmlfile = markdowner.convert(mdfile)
                    showentry = True
                    break
            # Display entry if found
            if showentry:
                return render(request, "encyclopedia/entry.html", {
                    "title": entry, "content": htmlfile, "form": form
                })
            else:
                results = []
                for entry in util.list_entries():
                    if input in entry:
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
                        "entries": results, "form": form
                    })
    else:
        form = SearchForm()
        content = "No search result was found."
        return render(request, "encyclopedia/error.html", {
            'form': form, 'content': content
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
