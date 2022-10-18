import re
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Category, Listing, Comment, Bid


def index(request):
    listings = Listing.objects.filter(is_active=True)
    return render(request, "auctions/index.html", {
        "listings": listings,
    })


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
    else:
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


def create_listing(request):
    if request.method == "GET":
        # Render "Create Listing" page
        categories = Category.objects.all()
        return render(request, "auctions/create.html", {
            "categories": categories
        })
    else:
        # Get data from the form
        title = request.POST["title"]
        description = request.POST["description"]
        description = re.sub("\n", "\n<br>", description)
        image_url = request.POST["image_url"]
        price = request.POST["price"]
        category = request.POST["category"]
        category = Category.objects.get(category_name=category)
        owner = request.user
        # Create a bid object
        bid = Bid(bid=float(price), user=owner)
        bid.save()
        # Create a listing object
        listing = Listing(
            title=title,
            description=description,
            image_url=image_url,
            price=bid,
            category=category,
            owner=owner
        )
        # Insert the listing object into database
        listing.save()
        # Redirect to index page
        return HttpResponseRedirect(reverse("index"))


def listing(request, id):
    # Get listing from database
    listing = Listing.objects.get(pk=id)
    user = request.user
    # Check if user is listing owner
    if user == listing.owner:
        is_owner = True
    else:
        is_owner = False
    # Check if listing is in watchlist
    users = listing.watchlist.all()
    if user in users:
        is_in_watchlist = True
    else:
        is_in_watchlist = False
    # Get comments from database
    comments = Comment.objects.filter(listing=listing)
    return render(request, "auctions/listing.html", {
    "listing": listing,
    "is_owner": is_owner,
    "is_in_watchlist": is_in_watchlist,
    "comments": comments,
    "user":user
    })


def add_to_watchlist(request, id):
    listing = Listing.objects.get(pk=id)
    user = request.user
    listing.watchlist.add(user)
    return HttpResponseRedirect(reverse("listing", args=(id, )))


def remove_from_watchlist(request, id):
    listing = Listing.objects.get(pk=id)
    user = request.user
    listing.watchlist.remove(user)
    return HttpResponseRedirect(reverse("listing", args=(id, )))


def watchlist(request):
    user = request.user
    # Get all listings in the watchlist of the user
    listings = user.watchlist.all()
    return render(request, "auctions/watchlist.html", {
    "listings": listings
    })


def bid(request, id):
    # Get new bid from form
    new_bid = float(request.POST["bid"])
    # Get listing from database
    listing = Listing.objects.get(pk=id)
    user = request.user
    # Check if user is listing owner
    is_owner = user == listing.owner
    # Check if listing is in watchlist
    is_in_watchlist = user in listing.watchlist.all()
    # Get cooments from database
    comments = Comment.objects.filter(listing=listing)
    # If new bid is higher than current one
    if new_bid > listing.price.bid:
        # save the bid
        bid = Bid(user=request.user, bid=new_bid)
        bid.save()
        # and update the listing
        listing.price = bid
        listing.save()
        return render(request, "auctions/listing.html", {
        "listing": listing,
        "is_owner": is_owner,
        "is_in_watchlist": is_in_watchlist,
        "comments": comments,
        "message": "Bid updated successfully!"
        })
    else:
        return render(request, "auctions/listing.html", {
        "listing": listing,
        "is_owner": is_owner,
        "is_in_watchlist": is_in_watchlist,
        "comments": comments,
        "message": "Your bid must be higher than current one!"
        })


def close_auction(request, id):
    listing = Listing.objects.get(pk=id)
    # Make listing inactive
    listing.is_active = False
    # Determine auction winner
    listing.winner = listing.price.user
    listing.save()
    user = request.user
    # Check if user is listing owner
    is_owner = user == listing.owner
    # Check if listing is in watchlist
    is_in_watchlist = user in listing.watchlist.all()
    # Get cooments from database
    comments = Comment.objects.filter(listing=listing)
    return render(request, "auctions/listing.html", {
        "listing": listing,
        "is_owner": is_owner,
        "is_in_watchlist": is_in_watchlist,
        "comments": comments,
        "user": user
        })

def comment(request, id):
    # Get comment data from form
    author = request.user
    listing = Listing.objects.get(pk=id)
    text = request.GET["text"]
    # Create new comment object
    comment = Comment(
        author=author,
        listing=listing,
        text=text
    )
    # Insert the comment object into database
    comment.save()
    # Redirect to listing page
    return HttpResponseRedirect(reverse("listing", args=(id, )))


def categories(request):
    # Get all categories
    categories = Category.objects.all()
    return render(request, "auctions/categories.html", {
        "categories": categories
    })


def category(request, id):
    # Get the category
    category = Category.objects.get(pk=id)
    # Get all listings in the category
    listings = Listing.objects.filter(is_active=True, category=category)
    return render(request, "auctions/category.html", {
    "category": category,
    "listings": listings
    })

