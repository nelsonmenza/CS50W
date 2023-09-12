from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.entry, name="entry"),
    path("random/", views.random_entry, name="random"),
    path("search/", views.search_entry, name="search"),
    path("new/", views.new_entry, name="new_entry"),
    path("edit/", views.edit, name="edit"),
    path("save_edit/", views.save_edit, name="save_edit"),
]
