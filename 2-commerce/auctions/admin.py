from django.contrib import admin

from .models import Listing, User

admin.site.register(Listing)
# admin.site.register(Category)
admin.site.register(User)
