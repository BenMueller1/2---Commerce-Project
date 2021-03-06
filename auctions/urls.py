from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("createListing", views.createListing, name="createListing"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("categories", views.categories, name="categories"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("categories/<str:category>", views.categoryPage, name="categoryPage"),
    path("listings/<int:listingId>", views.listingPage, name="listingPage")
]
