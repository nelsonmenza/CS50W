from django.contrib import admin

from .models import Bid, Comment, Listing, User, WatchlistItem

admin.site.register(Listing)
admin.site.register(Comment)
admin.site.register(User)
admin.site.register(Bid)
admin.site.register(WatchlistItem)
