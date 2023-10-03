from django.shortcuts import render
from django import forms
from markdown2 import Markdown

from . import util

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