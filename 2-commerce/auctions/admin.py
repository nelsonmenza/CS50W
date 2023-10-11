from django.contrib import admin

from .models import Comment, Listing, User

admin.site.register(Listing)
admin.site.register(Comment)
admin.site.register(User)
