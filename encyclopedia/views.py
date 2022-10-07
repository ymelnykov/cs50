from django.shortcuts import render
from markdown2 import Markdown
from random import choice

from . import util


def index(request):
    entries = util.list_entries()
    return render(request, "encyclopedia/index.html", {
        "title": 'All Pages',
        "entries": entries
    })

def entry(request, entry):
    entry_page = util.get_entry(entry)
    if entry_page is None:
        return render(request, "encyclopedia/error.html", {
            "message": 'Page not found!'
        })
    else:
        return render(request, "encyclopedia/entry.html", {
            "entry": Markdown().convert(entry_page),
            "entry_title": entry
        })

def search(request):
    if request.method == "POST":
        query = request.POST['q']
        query_page = util.get_entry(query)
        if query_page:
            return render(request, "encyclopedia/entry.html", {
                "entry": Markdown().convert(query_page),
                "entry_title": query
            })
        else:
            entries = util.list_entries()
            sub_entries = []
            for entry in entries:
                if query.upper() in entry.upper():
                    sub_entries.append(entry)
            if sub_entries:
                return render(request, "encyclopedia/index.html", {
                    "title": 'Search Results',
                    "entries": sub_entries
                })
            else:
                return render(request, "encyclopedia/error.html", {
                    "message": 'Page not found!'
                })

def new_page(request):
    if request.method == "POST":
        title = request.POST['title']
        content = request.POST['content']
        if util.get_entry(title):
            return render(request, "encyclopedia/error.html", {
                    "message": 'Encyclopedia entry with such title already exists!'
            })
        else:
            util.save_entry(title, content)
            return render(request, "encyclopedia/entry.html", {
                "entry": Markdown().convert(content),
                "entry_title": title
            })
    else:
        return render(request, "encyclopedia/new_page.html")

def edit(request):
    if request.method == "GET":
        entry = request.GET['entry']
        entry_page = util.get_entry(entry)
        return render(request, "encyclopedia/edit.html", {
                "entry_page": entry_page,
                "entry_title": entry
        })
    else:
        title = request.POST['title']
        content = request.POST['content']
        util.save_entry(title, content)
        return render(request, "encyclopedia/entry.html", {
            "entry": Markdown().convert(content),
            "entry_title": title
        })

def random_page(request):
    entries = util.list_entries()
    entry = choice(entries)
    entry_page = util.get_entry(entry)
    return render(request, "encyclopedia/entry.html", {
            "entry": Markdown().convert(entry_page),
            "entry_title": entry
        })



            


