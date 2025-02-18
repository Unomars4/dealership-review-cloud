from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
from .models import CarMake, CarModel
from .restapis import get_dealers_from_cf, get_dealer_reviews_from_cf, post_request
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
import logging
import json
import os
import random

dealers_url = os.environ.get("DEALERSHIPS_API")
reviews_url = os.environ.get("REVIEWS_API")
post_review_url = os.environ.get("POST_REVIEW")

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
    context = {}

    if request.method == "GET":
        dealerships = get_dealers_from_cf(dealers_url)
        context["dealerships"] = dealerships
        return render(request, 'djangoapp/index.html', context)


def get_dealer_details(request, dealer_id):
    context = {}
    if request.method == "GET":
        dealerships = get_dealers_from_cf(dealers_url)
        dealer_details = [dealer for dealer in dealerships if dealer.id == dealer_id]
        dealer_reviews = get_dealer_reviews_from_cf(reviews_url, dealer_id)
        context["dealer"] = dealer_details[0]
        context["dealer_id"] = dealer_id
        context["dealer_reviews"] = dealer_reviews
        return render(request, 'djangoapp/dealer_details.html', context)

def add_review(request, dealer_id):
    context = {}
    
    if request.method == "GET":
        
        dealerships = get_dealers_from_cf(dealers_url)
        dealer_details = [dealer for dealer in dealerships if dealer.id == dealer_id]
        context["cars"] = CarModel.objects.filter(dealer_id=dealer_id)
        context["dealer"] = dealer_details[0]
        
        return render(request, "djangoapp/add_review.html", context)
    
    elif request.method == "POST":
        data = request.POST
        
        if request.user.is_authenticated:
            
            car_data = CarModel.objects.get(id = data["car"][0])
            car_make = CarMake.objects.get(id = car_data.car_make_id)
            review = {
                "id": random.randint(1,10000),
                "name": "John Doe", 
                "dealership": dealer_id,
                "review": data["review"],
                "car_make": car_make.name,
                "car_model": car_data.name,
                "car_year": car_data.year.strftime("%Y"),
                "purchase": data["purchase"][0] == "on",
                "purchase_date": data["purchasedate"]
            } 
            json_payload = review
            response = post_request(post_review_url, json_payload, dealerId=dealer_id)
            
            return redirect('djangoapp/dealer_details.html', dealer_id=dealer_id)
        else:
            return HttpResponse("User not logged in")        

