from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.decorators import method_decorator
from django.views import View

from .forms import BidForm, CommentForm, ListingForm
from .models import Bid, Comment, Listing, User, WatchlistItem


def index(request):
    listings = Listing.objects.all().filter(active=True)
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
    list_categories = [c[0] for c in Listing.categories.field.choices]
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
    return render(request, 'auctions/create_listing.html', {'form': form, 'list_categories': list_categories})


def categories_list(request, categories):
    categories_lst = Listing.objects.all().filter(
        categories=categories).filter(active=True)
    list_categories = [c[0] for c in Listing.categories.field.choices]
    context = {"categories_lst": categories_lst,
               "categories": categories, "list_categories": list_categories}
    return render(request, "auctions/categories_list.html", context)


class DetailListingView(View):
    def get(self, request, pk):
        listing = get_object_or_404(Listing, pk=pk)
        print(listing)
        comments = Comment.objects.filter(post_id=pk)
        form = CommentForm()
        list_categories = [c[0] for c in Listing.categories.field.choices]
        context = {"listing": listing, 'form': form,
                   "list_categories": list_categories, "comments": comments}
        return render(request, "auctions/detail.html", context)

    @method_decorator(login_required)
    def post(self, request, pk):
        listing = get_object_or_404(Listing, pk=pk)
        comments = Comment.objects.filter(post_id=pk)
        form = CommentForm(request.POST)
        bid_form = BidForm(request.POST)  # Handle the bid form data

        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.username = request.user
            new_comment.post = listing
            new_comment.save()
            return redirect('detail', pk=listing.pk)

        if bid_form.is_valid():  # Handle the bid form's validation
            bid_amount = bid_form.cleaned_data['amount']
            # Create a new Bid object and associate it with the listing
            new_bid = Bid.objects.create(
                post_listing_bid=listing, user=request.user, amount=bid_amount)
            new_bid.save()
            return redirect('detail', pk=listing.pk)

        list_categories = [c[0] for c in Listing.categories.field.choices]
        context = {
            "listing": listing,
            'form': form,
            'bid_form': bid_form,  # Add the bid form to the context
            "list_categories": list_categories,
            "comments": comments
        }
        return render(request, "auctions/detail.html", context)


def add_to_watchlist(request, pk):
     watchlist_lst = Listing.objects.all().filter(
        categories=categories).filter(active=True)
    watchlist_lst = WatchlistItem.objects.all().filter(listing_id=pk)
    if request.method == "POST":
        watchlist = WatchlistItem.objects.create(
            listing=listing, user=request.user)
        watchlist.save()
    # Redirect to the listing detail page
        return redirect('watchlist', pk=pk)
    else:
        watchlist = WatchlistItem()
        return render(request, "auctions/watchlist_listing.html", {"watchlist": watchlist})


def remove_from_watchlist(request, pk):
    if request.user.is_authenticated:
        WatchlistItem.objects.filter(
            user=request.user, listing_id=pk).delete()
    return redirect('detail', pk=pk)
