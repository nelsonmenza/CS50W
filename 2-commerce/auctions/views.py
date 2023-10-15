from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.decorators import method_decorator
from django.views import View

from .forms import BidForm, CommentForm, ListingForm
from .models import Bid, Comment, Listing, User, WatchlistItem


# View for the home page
def index(request):
    """
    Render the home page with active listings.
    """
    listings = Listing.objects.all().filter(active=True)
    list_categories = [c[0] for c in Listing.categories.field.choices]
    context = {"listings": listings, "list_categories": list_categories}
    return render(request, "auctions/index.html", context)

# View for user login


def login_view(request):
    """
    Handle user login.
    """
    if request.method == "POST":
        # Attempt to sign the user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication is successful
        if user is not None:
            login(request, user)
            return redirect("index")
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")

# View for user logout


def logout_view(request):
    """
    Handle user logout.
    """
    logout(request)
    return redirect("index")

# View for user registration


def register(request):
    """
    Handle user registration.
    """
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

        # Attempt to create a new user
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

# View for creating a new listing


def create_listing(request):
    """
    Create a new listing.
    """
    list_categories = [
        c[0] for c in Listing.Categories.choices]  # Use .Categories.choices to access choices

    if request.method == 'POST':
        form = ListingForm(request.POST, request.FILES)
        if form.is_valid():
            listing = form.save(commit=False)
            listing.username = request.user
            listing.save()
            return redirect('index')

    else:
        form = ListingForm()

    context = {'form': form, 'list_categories': list_categories}
    return render(request, 'auctions/create_listing.html', context)

# View for listing categories


def categories_list(request, categories):
    """
    List items by a specific category.
    """
    categories_lst = Listing.objects.all().filter(
        categories=categories).filter(active=True)
    list_categories = [c[0] for c in Listing.categories.field.choices]
    context = {"categories_lst": categories_lst,
               "categories": categories, "list_categories": list_categories}
    return render(request, "auctions/categories_list.html", context)

# View for listing details and comments


class DetailListingView(View):
    """
    Show listing details and handle comments.
    """

    def get(self, request, pk):
        # Render the listing details
        listing = get_object_or_404(Listing, pk=pk)
        comments = Comment.objects.filter(post_id=pk)
        form = CommentForm()
        list_categories = [c[0] for c in Listing.categories.field.choices]
        context = {"listing": listing, 'form': form,
                   "list_categories": list_categories, "comments": comments}
        return render(request, "auctions/detail.html", context)

    @method_decorator(login_required)
    def post(self, request, pk):
        # Handle comments and bids
        listing = get_object_or_404(Listing, pk=pk)
        comments = Comment.objects.filter(post_id=pk)
        form = CommentForm(request.POST)
        bid_form = BidForm(request.POST)  # Handle the bid form data
        message = ""  # Initialize the message

        if form.is_valid():
            # Handle comments
            new_comment = form.save(commit=False)
            new_comment.username = request.user
            new_comment.post = listing
            new_comment.save()
            return redirect('detail', pk=listing.pk)

        if bid_form.is_valid():  # Handle the bid form's validation
            bid_amount = bid_form.cleaned_data['amount']

            if bid_amount > listing.starting_bid:
                # Create a new Bid object and associate it with the listing
                new_bid = Bid.objects.create(
                    post_listing_bid=listing, user=request.user, amount=bid_amount)

                new_bid.save()
                listing.starting_bid = new_bid.amount
                listing.save()
                message = "The bid was accepted, Good luck. "
                return redirect('detail', pk=listing.pk)
            else:
                message = "The bid was denied, try another amount. "

        list_categories = [c[0] for c in Listing.categories.field.choices]
        context = {
            "listing": listing,
            'form': form,
            'bid_form': bid_form,
            "list_categories": list_categories,
            "comments": comments,
            "message": message
        }
        return render(request, "auctions/detail.html", context)

# Watchlist functionality


def add_to_watchlist(request, pk):
    """
    Add a listing to the user's watchlist.
    """
    listing = get_object_or_404(Listing, pk=pk)
    if request.method == "POST":
        WatchlistItem.objects.get_or_create(
            listing=listing, user=request.user)
        return redirect('watchlist')


def remove_from_watchlist(request, pk):
    """
    Remove a listing from the user's watchlist.
    """
    listing = get_object_or_404(Listing, pk=pk)
    if request.method == "POST":
        WatchlistItem.objects.filter(
            user_id=request.user, listing_id=listing.pk).delete()
    return redirect('detail', pk=pk)


def get_watchlist(request):
    """
    Show the user's watchlist.
    """
    listings = WatchlistItem.objects.all().filter(user_id=request.user)
    list_categories = [c[0] for c in Listing.categories.field.choices]
    context = {"listings": listings, "list_categories": list_categories}
    return render(request, "auctions/watchlist_listing.html", context)

# Close auctions functionality


@login_required
def close_auction(request, pk):
    listing = get_object_or_404(Listing, pk=pk)
    bid = get_object_or_404(Bid, post_listing_bid=pk,
                            amount=listing.starting_bid)
    print(bid.user)
    if request.method == "POST":
        if request.user == listing.username:
            # Check if the user is the owner of the listing
            if listing.active:
                # Check if the listing is active
                highest_bid_amount = listing.get_highest_bid_amount()
                print(highest_bid_amount)
                if highest_bid_amount is not None:
                    # Set the highest bidder as the winner
                    listing.winner = bid.user
                listing.active = False
                listing.save()
                WatchlistItem.objects.get_or_create(
                    listing=listing, user=bid.user)
                return redirect('index')
            else:
                return redirect('index')
    else:
        return redirect('detail', pk=listing.pk)
