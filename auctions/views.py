from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import forms

from . import models

from .models import User

class newListingForm(forms.Form):
    title = forms.CharField(label="Listing title")
    description = forms.CharField(label="Listing description", widget=forms.Textarea(attrs={"rows":5, "cols":60}))
    startingBid = forms.FloatField(label="Starting Bid", min_value = 0.01)
    category = forms.CharField(label="Category", required=False)   # could change this to a choice field if we want
    image = forms.URLField(label="Image URL", required=False)


def index(request):
    return render(request, "auctions/index.html")


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:  # if request.method == "GET"
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


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
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")



def createListing(request):
    if request.method == "POST":
        # need to make a copy of request.POST without the csrfmiddlewaretoken entry (can't just delete bc request.POST is immutable)
        data = {}
        for k in request.POST.keys():
            if k != "csrfmiddlewaretoken":
                data[k] = request.POST[k]
        listing = models.Listing(**data)  # can you pass a dictionary in? or do I have to pass in each field individually? YES! If we use **
        listing.save()
        return(HttpResponseRedirect(reverse("index")))

    else:
        form = newListingForm()
        context = {"form": form}
        return render(request, "auctions/newListing.html", context)


