from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator
from django.db import models
from django.db.models import Max


class User(AbstractUser):
    pass


class Listing(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=1000)
    username = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    starting_bid = models.DecimalField(max_digits=6, decimal_places=2, validators=[
        MinValueValidator(0.50)], blank=False)

    web_page = models.URLField(max_length=200, blank=True)
    img = models.ImageField(null=True, blank=True, upload_to='media/')
    active = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now_add=True)

    class Categories(models.TextChoices):
        CLOTHING = 'Clothing'
        TOYS = 'Toys'
        GAMES = 'Games'
        ELECTRONICS = 'Electronics'
        HOME = 'Home'
        SPORTS = 'Sports'
        BEAUTY = 'Beauty'
        BOOKS = 'Books'
        GROCERY = 'Grocery'
        AUTOMOTIVE = 'Automotive'
        HEALTH = 'Health'

    categories = models.CharField(max_length=100, choices=Categories.choices)

    winner = models.ForeignKey(User, null=True, blank=True,
                               related_name="won_listings", on_delete=models.SET_NULL)

    def get_highest_bid_amount(self):
        """
        Get the highest bid amount for this listing, if it exists.

        Returns:
            Decimal: The highest bid amount or None if no bids exist.
        """
        highest_bid = self.bid_set.aggregate(Max('amount'))['amount__max']
        return highest_bid

    class Meta:
        verbose_name = 'Listing'
        verbose_name_plural = 'Listings'

    def __str__(self):
        return 'Listing  {} by {}'.format(self.title, self.username)


class Comment(models.Model):
    username = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    body = models.TextField(max_length=350)
    created_date = models.DateTimeField(auto_now_add=True)
    post = models.ForeignKey(
        Listing, on_delete=models.CASCADE, related_name='comments')

    class Meta:
        ordering = ['created_date']

    def __str__(self):
        return 'Comment in listing {} by {}'.format(self.post, self.username)


class Bid(models.Model):
    amount = models.DecimalField(max_digits=6, decimal_places=2, validators=[
        MinValueValidator(0.50)])
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    post_listing_bid = models.ForeignKey(
        Listing, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Bid'

    def __str__(self):
        return 'Bid in listing {} by {}'.format(self.post_listing_bid, self.user)


class WatchlistItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Watchlist'

    def __str__(self):
        return 'Watchlist for user {}'.format(self.user)
