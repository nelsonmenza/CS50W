import random

from django.shortcuts import render
from markdown2 import Markdown

from . import util


# Define the index view that renders a list of encyclopedia entries
def index(request):
    """
    Renders the main encyclopedia index page.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: A response containing the rendered HTML template with a list of encyclopedia entries.
    """
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

# Define the entry view that displays the content of a specific encyclopedia entry


def entry(request, title):
    """
    Renders the page for a specific encyclopedia entry.

    Args:
        request (HttpRequest): The HTTP request object.
        title (str): The title of the encyclopedia entry to be displayed.

    Returns:
        HttpResponse: A response containing the rendered HTML template with the content of the specified entry.
    """
    markdowner = Markdown()
    page = util.get_entry(title)
    if page is None:
        return render(request, "encyclopedia/error.html",
                      {"title": "Page not found",
                       "content": "Page does not exist or was not found."})
    else:
        page_converted = markdowner.convert(page)
        return render(request, "encyclopedia/entry.html", {"content": page_converted,
                                                           "title": title})

# Define a view to display a random encyclopedia entry


def random_entry(request):
    """
    Redirects to a random encyclopedia entry.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: A response that redirects to a randomly selected encyclopedia entry page.
    """
    entry_list = util.list_entries()
    random_entry = random.choice(entry_list)
    return entry(request, random_entry)

# Define a view to search for encyclopedia entries


def search_entry(request):
    """
    Searches for encyclopedia entries based on user input.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: A response containing search results or an error message if no results are found.
    """
    entry_list = util.list_entries()
    if request.method == "POST":
        title = request.POST["q"]
        if title in entry_list:
            return entry(request, title)
        else:
            lst = []
            for entri in entry_list:
                if title.lower() in entri.lower():
                    lst.append(entri)
            if not lst:
                return render(request, "encyclopedia/error.html",
                              {"title": "Search",
                               "content": "Page does not exist or was not found."})
            else:
                return render(request, "encyclopedia/search.html", {"entries": lst,
                                                                    "title": "Search Suggestions"})

# Define a view to create a new encyclopedia entry


def new_entry(request):
    """
    Renders the page for creating a new encyclopedia entry or processes the form submission.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: A response containing the new entry or an error message if the entry already exists.
    """
    if request.method == "GET":
        return render(request, "encyclopedia/new_entry.html")
    else:
        title = request.POST["title"]
        content = request.POST["content"]
        entry_exist = util.get_entry(title)
        if entry_exist is None:
            util.save_entry(title, content)
            return entry(request, title)
        else:
            return render(request, "encyclopedia/error.html",
                          {"title": "New page",
                           "content": "Page already exists",
                           "information": "Change the title or edit the current entry."
                           })

# Define a view to edit an existing encyclopedia entry


def edit(request):
    """
    Renders the page for editing an existing encyclopedia entry.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: A response containing the content of the entry to be edited.
    """
    if request.method == "POST":
        title = request.POST["entry_title"]
        content = util.get_entry(title)
        return render(request, "encyclopedia/edit.html", {"title": title,
                                                          "content": content})

# Define a view to save changes made to an edited entry


def save_edit(request):
    """
    Saves the changes made to an edited encyclopedia entry.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: A response that redirects to the edited entry page.
    """
    if request.method == "POST":
        title = request.POST["title"]
        content = request.POST["content"]
        util.save_entry(title, content)
        return entry(request, title)
