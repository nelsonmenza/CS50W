from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.shortcuts import get_object_or_404, redirect, render

from .forms import CommentForm, ListingForm
from .models import Comment, Listing, User


def index(request):
    listings = Listing.objects.all()
    list_categories = [c[0] for c in Listing.categories.field.choices]
    context = {"listings": listings, "list_categories": list_categories}
    return render(request, "auctions/index.html", context)


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return redirect("index")
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return redirect("index")


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return redirect("index")
    else:
        return render(request, "auctions/register.html")


@login_required
def create_listing(request):
    if request.method == 'POST':
        form = ListingForm(request.POST, request.FILES)
        print(form)
        if form.is_valid():
            listing = form.save(commit=False)
            listing.username = request.user
            listing.save()
            return redirect('index')
    else:
        form = ListingForm()
    return render(request, 'auctions/create_listing.html', {'form': form})


def categories_list(request, categories):
    categories_lst = Listing.objects.all().filter(categories=categories)
    list_categories = [c[0] for c in Listing.categories.field.choices]
    context = {"categories_lst": categories_lst,
               "categories": categories, "list_categories": list_categories}
    return render(request, "auctions/categories_list.html", context)


def detail_listing(request, pk):
    listing = get_object_or_404(Listing, pk=pk)
    comments = Comment.objects.all().filter(post_id=pk)
    new_comment = None    # Comment posted

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.username = request.user
            new_comment.post = listing
            new_comment.save()
            return redirect('show:detail', kwargs={'show': instance.pk})
    else:
        form = CommentForm()
    list_categories = [c[0] for c in Listing.categories.field.choices]
    context = {"listing": listing, 'form': form,
               "list_categories": list_categories, "comments": comments}
    return render(request, "auctions/detail.html", context)
