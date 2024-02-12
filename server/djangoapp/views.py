from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
# from .models import User
from .restapis import get_dealers_from_cf, get_dealer_reviews_from_cf, post_request
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
import logging
import json
import os

logger = logging.getLogger(__name__)

def static_page(request):
    context = {}
    if request.method == "GET":
        return render(request, "djangoapp/static.html", context)


def about(request):
    context = {}
    if request.method == "GET":
        return render(request, "djangoapp/about.html", context)


def contact(request):
    context = {}
    if request.method == "GET":
        return render(request, "djangoapp/contact.html", context)


def login_request(request):
    context = {}
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["psw"]

        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("djangoapp:index")
        else:
            return render(request, "djangoapp/index.html", context)
    else:
        return render(request, "django/index.html", context)

def logout_request(request):
    logout(request)
    return redirect("djangoapp:index")


def registration_request(request):
    context = {}
    if request.method == "GET":
        return render(request, "djangoapp/registration.html", context)
    elif request.method == "POST":
        username, firstname, lastname, password = request.POST.values()
        user_exists = False
        try:
            user = User.objects.get(username=username)
            if user is not None:
                user_exists = True
        except:
            logger.debug(f"{username} is already taken")
        
        if not user_exists:
            try:
                user = User.objects.create_user(username=username, first_name=firstname, last_name=lastname, password=password)
            except Error:
                logger.debug(f"Couldn't create user, because {Error}")
            return redirect("djangoapp:index")
        else:
            return render(request, "djangoapp/registration.html", context)

def get_dealerships(request):
    if request.method == "GET":
        url = os.environ.get("DEALERSHIPS_API")
        # Get dealers from the URL
        dealerships = get_dealers_from_cf(url)
        # Concat all dealer's short name
        dealer_names = ' '.join([dealer.short_name for dealer in dealerships])
        # Return a list of dealer short name
        return HttpResponse(dealer_names)


def get_dealer_details(request, dealer_id):
    if request.method == "GET":
        url = os.environ.get("REVIEWS_API")
        dealer_reviews = get_dealer_reviews_from_cf(url, dealer_id)
        reviews = "\n".join([f"{review.review},  {review.sentiment}" for review in dealer_reviews])
        return HttpResponse(reviews)

def add_review(request, dealer_id):
    url = os.environ.get("POST_REVIEW")
    
    if request.method == "POST":
        if request.user.is_authenticated:
            review = {t
            for field in request.body.keys():
                review[field] = request.body[field].body.yearyear''""CAcar_                ,            }
            json_payload = {"review":review}
            response = post_request(url, json_payload, dealerId=dealer_id)
            return HttpResponse(response)
        else:
            return HttpResponse("User not logged in")        

