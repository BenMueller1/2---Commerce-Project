from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import forms
from django.contrib.auth.decorators import login_required

from . import models

from .models import User

class newListingForm(forms.Form):
    title = forms.CharField(label="Listing title")
    description = forms.CharField(label="Listing description", widget=forms.Textarea(attrs={"rows":3, "cols":60}))
    startingBid = forms.FloatField(label="Starting Bid", min_value = 0.01)
    category = forms.CharField(label="Category", required=False)   # could change this to a choice field if we want
    image = forms.URLField(label="Image URL", required=False)

class newBidForm(forms.Form):
    bid = forms.FloatField(label="New bid: ", min_value=0.01)

class newCommentForm(forms.Form):
    comment = forms.CharField(label="New Comment: ", widget=forms.Textarea(attrs={"rows":5, "cols":30}))
    title = forms.CharField(label= "Comment Title: ")

def index(request):
    listings = models.Listing.objects.all()
    context = {"listings": listings}
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
        listing.currentBid = listing.startingBid
        listing.creator = request.user
        listing.highestBidder = request.user
        listing.save()
        return(HttpResponseRedirect(reverse("index")))

    else:
        form = newListingForm()
        context = {"form": form}
        return render(request, "auctions/newListing.html", context)


def categories(request):
    all_categories = []
    # go through all Listing models, each time a category isn't in the list, add it (case insensitive)
    allListings = models.Listing.objects.all()
    for listing in allListings:
        if listing.category.lower() not in all_categories:
            all_categories.append(listing.category.lower())
    context = {"categories": all_categories}
    return render(request, "auctions/categories.html", context)

def watchlist(request):
    return render(request, "auctions/watchlist.html")

def categoryPage(request, category):
    context = {"category": category} # going to display a list of every listing that has this as a category
    listingsInCategory = []
    allListings = models.Listing.objects.all()
    for listing in allListings:
        if listing.category.lower() == category.lower():
            listingsInCategory.append(listing)
    context["listingsInCategory"] = listingsInCategory
    return render(request, "auctions/categoryPage.html", context)


@login_required
def listingPage(request, listingId):
    listing = models.Listing.objects.filter(id=listingId)[0]

    if request.method == "POST":
        # this will be POST if the form to add to watchlist or the form to change bid was submitted 
        # check for what data is passed in the POST request to decide what to do, then redirect to this page? (do I have to redirect? I don't think so)

        post_request_keys = request.POST.keys()
        if "comment" in post_request_keys:
            newComment = models.Comment(user=request.user, title=request.POST['title'], text=request.POST['comment'])
            newComment.save()   # this is causing an error
            listing.comments.add(newComment)

        elif "bid" in post_request_keys:
            if float(request.POST['bid']) > listing.currentBid:
                listing.currentBid = request.POST['bid']
                listing.highestBidder = request.user

        elif "addToWishList" in post_request_keys:
            request.user.watchlist.add(listing)


    if len(models.Listing.objects.filter(id=listingId)) == 0:
        context = {"listingId": listingId}
        return render(request, "auctions/noSuchListing.html", context)
    
    bidForm = newBidForm()
    commentForm = newCommentForm()
    context = {"listing": listing, "bidForm":bidForm, "commentForm": commentForm, "comments":listing.comments}

    return render(request, "auctions/listingPage.html", context)