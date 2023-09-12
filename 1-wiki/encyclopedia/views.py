import random

from django.shortcuts import render
from markdown2 import Markdown

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()})


def entry(request, title):
    markdowner = Markdown()
    page = util.get_entry(title)
    if page == None:
        return render(request, "encyclopedia/error.html",
                      {"title": "Page not found",
                       "content": "Page not exist or not found."})
    else:
        page_converted = markdowner.convert(page)
        return render(request, "encyclopedia/entry.html", {"content": page_converted,
                                                           "title": title})


def random_entry(request):
    entry_list = util.list_entries()
    random_entry = random.choice(entry_list)
    return entry(request, random_entry)


def search_entry(request):
    entry_list = util.list_entries()
    if request.method == "POST":
        title = request.POST["q"]
        if title in entry_list:
            return entry(request, title)
        else:
            lst = []
            for entry in entry_list:
                if title.lower() in entry.lower():
                    print(entry)
                    lst.append(entry)
            if lst == []:
                return render(request, "encyclopedia/error.html",
                              {"title": "Search",
                               "content": "Page not exist or not found."})
            else:
                return render(request, "encyclopedia/search.html", {"entries": lst,
                                                                    "title": "search suggection"})


def new_entry(request):
    if request.method == "GET":
        return render(request, "encyclopedia/new_entry.html")
    else:
        title = request.POST["title"]
        content = request.POST["content"]
        entry_exist = util.get_entry(title)
        if entry_exist == None:
            util.save_entry(title, content)
            return entry(request, title)
        else:
            return render(request, "encyclopedia/error.html",
                          {"title": "New page",
                           "content": "Page already exist",
                           "information": "Change the title or edit the current entry."
                           })


def edit(request):
    if request.method == "POST":
        title = request.POST["entry_title"]
        content = util.get_entry(title)
        return render(request, "encyclopedia/edit.html", {"title": title,
                                                          "content": content})


def save_edit(request):
    if request.method == "POST":
        title = request.POST["title"]
        content = request.POST["content"]
        util.save_entry(title, content)
        return entry(request, title)
