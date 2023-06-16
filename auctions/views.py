from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .models import User, Item, Watchlist, Bid, Message, Item_Message_Group

# In house functions

def isowner(request, item_id):
    item = Item.objects.get(id = item_id)
    if request.user == item.poster:
        owner=True
    else:  
        owner=False
    return owner

def find_bidder(item_id):
    item = Item.objects.get(id = item_id)
    bid = Bid.objects.get(item = item)
    current_bidder = bid
    return current_bidder

def get_messages(item_id):
    message_group = Item_Message_Group.objects.get(item = item_id)
    return message_group.messages
# __________________________________________
def index(request):
    return render(request, "auctions/index.html", {
        "items": Item.objects.all()
    })

def product(request, item_id):
    item = Item.objects.get(id = item_id)
    items = Watchlist.objects.get(user = request.user)
    watchlist = items.watchlist
    in_watchlist = False
    for items in watchlist.all():
        if items == item:
            in_watchlist = True
    return render(request, "auctions/product.html", {
        "item": item,
        "in_watchlist": in_watchlist,
        "owner": isowner(request, item_id),
        "last_bidder": find_bidder(item_id).bidder,
        "messages": get_messages(item_id).all
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
            watchlist = Watchlist.objects.create(user = User.objects.get(username = username))
            watchlist.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

@login_required
def create(request):
    if request.method == "POST":
        category = request.POST["category"].lower()
        title = request.POST["title"]
        price = request.POST["price"]
        description = request.POST["description"]
        image= request.POST["image"]
        if not title or price or description:
            if not category:
                item = Item(title=title, price=price, description=description, poster = request.user)
            else:
                item = Item(category=category, title=title, price=price, description=description, poster = request.user)

            item.name = title
            item.closed = False
            bid_item = Bid(item =item, bidder=request.user)

            message_group = Item_Message_Group(item = item)

            if not image:
                item.save()
                message_group.save()
                bid_item.save()
                return HttpResponseRedirect(reverse("index"))
            else:
                item.image = image
                item.save()
                message_group.save()
                bid_item.save()
                return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/create.html", {
                "message": "Fill in all fields."
            })
    return render(request, "auctions/create.html")

def close(request, item_id):
    item = Item.objects.get(id = item_id)
    item.closed = True
    item.save()
    return product(request, item_id)

@login_required
def bid(request, item_id):
    if request.method == "POST":
        item = Item.objects.get(id = item_id)
        new_price=int(request.POST["price"])
        watchlist = Watchlist.objects.get(user = request.user).watchlist
        in_watchlist = False
        for items in watchlist.all():
            if items == item:
                in_watchlist = True

        if item.price < new_price:
            bid_item = find_bidder(item_id)
            bid_item.bidder = request.user
            bid_item.save()
            item.price = new_price
            item.save()
            return render(request, "auctions/product.html", {
            "item_name": item.title,
            "valid": "Bid succesfully placed",
            "item": item,
            "in_watchlist": in_watchlist,
            "owner": isowner(request, item_id),
            "messages": get_messages(item_id).all
            })
        if item.price > new_price:
            return render(request, "auctions/product.html", {
            "item_name": item.title,
            "invalid": "Invalid Price",
            "item": item,
            "in_watchlist": in_watchlist,
            "owner": isowner(request, item_id),
            "messages": get_messages(item_id).all
            })
        else:
            return HttpResponseRedirect(reverse('product', args=[item_id]))
    else:
        return HttpResponseRedirect(reverse('product', args=[item_id]))
    
def comment(request, item_id):
    if request.method == "POST":
        message = request.POST["comment"]
        if len(message) > 0:
            new_message  = Message.objects.create(user = request.user, message = message)
            message_group = Item_Message_Group.objects.get(item = item_id).messages
            message_group.add(new_message)
            return HttpResponseRedirect(reverse('product', args=[item_id]))
        return HttpResponseRedirect(reverse('product', args=[item_id]))

    
@login_required
def add_watchlist(request, item_id):
    add_item = Item.objects.get(id = item_id)
    # user_list = Watchlist.objects.get(user = User.objects.get(username = "Something"))
    user_list = Watchlist.objects.get(user = request.user)
    user_list.watchlist.add(add_item)
    return HttpResponseRedirect(reverse('product', args=[item_id]))

@login_required
def remove(request, item_id):
    add_item = Item.objects.get(id = item_id)
    # user_list = Watchlist.objects.get(user = User.objects.get(username = "Something"))
    user_list = Watchlist.objects.get(user = request.user)
    user_list.watchlist.remove(add_item)
    return HttpResponseRedirect(reverse('product', args=[item_id]))

@login_required
def watchlist(request):
    items = Watchlist.objects.filter(user = request.user)
    if items is None:
        return render(request, "auctions/watchlist.html", {})
    
    items = Watchlist.objects.get(user = request.user)
    watchlist = items.watchlist
    return render(request, "auctions/watchlist.html", {
        "watchlist": watchlist.all
        })


def category(request):
    categories = set()
    for item in Item.objects.all():
        categories.add(item.category)

    return render(request, "auctions/category.html", {
        "categories": categories,
    })

def chosen_category(request, category):
    items = Item.objects.filter(category = category)
    return render(request, "auctions/index.html", {
        "items": items
    })