from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create_listing", views.create_listing, name="create_listing"),
    path("categories/<str:categories>/",
         views.categories_list, name="categories_list"),
    path("detail/<int:pk>/",
         views.DetailListingView.as_view(), name="detail"),
    path("watchlist/<int:pk>/",
         views.add_to_watchlist, name="watchlist"),
    path('remove_from_watchlist/<int:pk>/',
         views.remove_from_watchlist, name='remove_from_watchlist'),




]
