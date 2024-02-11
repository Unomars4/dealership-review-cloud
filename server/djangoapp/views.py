from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
# from .models import User
# from .restapis import rela
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
import logging
import json

# Get an instance of a logger
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

# Update the `get_dealerships` view to render the index page with a list of dealerships
def get_dealerships(request):
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/index.html', context)


# Create a `get_dealer_details` view to render the reviews of a dealer
# def get_dealer_details(request, dealer_id):
# ...

# Create a `add_review` view to submit a review
# def add_review(request, dealer_id):
# ...

