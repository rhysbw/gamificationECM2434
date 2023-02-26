from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.exceptions import ObjectDoesNotExist

from .forms import SignupForm
from exSeed.models import Spot, PreviousSpotAttend
import random

from user_agents import parse

import datetime

# Create your views here.
def signup(request):
    # Checks if the user is on a desktop instead of mobile and if
    # so renders the QR code page
    user_agent = parse(request.META['HTTP_USER_AGENT'])
    if not user_agent.is_mobile:
        return render(request, 'QRCodePage.html')

    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = SignupForm()
    return render(request, 'signup.html', {"register_form": form})


def login_request(request):
    # Checks if the user is on a desktop instead of mobile and if
    # so renders the QR code page
    user_agent = parse(request.META['HTTP_USER_AGENT'])
    if not user_agent.is_mobile:
        return render(request, 'QRCodePage.html')

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.error(request, "Invalid username or password")
        else:
            messages.error(request, "Invalid username or password")
    form = AuthenticationForm()
    return render(request=request, template_name='registration/login.html', context={"login_form": form})


def logout_request(request):
    logout(request)
    messages.info(request, "You have successfully logged out")
    return redirect('home')


def delete_request(request, username):
    try:
        user = User.objects.get(username=username)
        user.delete()
    except Exception as e:
        messages.error(request, f"Failed to delete user: {e}")
    return redirect('home')


def home_page(request):
    # Checks if the user is on a desktop instead of mobile and if
    # so renders the QR code page
    user_agent = parse(request.META['HTTP_USER_AGENT'])
    if not user_agent.is_mobile:
        return render(request, 'QRCodePage.html')

    # Checks if the user is logged in or not, if not they are automatically redirected
    # to the login page
    if not request.user.is_authenticated:
        return redirect('/login')

    #Find todays spot
    today = datetime.date.today()

    #Checks if there is a spot for today and if not a new one will be assigned
    try:
        spot = PreviousSpotAttend.objects.filter(spotDay=today).first().sId
        print(spot)
        print("spot was already assigned")
    except:
        print("spot was not assigned")
        yesterday = today - datetime.timedelta(days=1)
        while True:
            # pick a random spot
            spot = random.choice(Spot.objects.all())
            # check if that is the same as yesterday and if so get a new one
            try:
                print("here")
                if spot.id != PreviousSpotAttend.objects.filter(spotDay=yesterday)[0].sId:
                    False
            except:
                break
        PreviousSpotAttend(sId=spot, attendance=0, spotDay=today).save()
        print("spot of the day assigned")



    #Assigns the values of todays spot so they can be rendered into the website
    spot_name = spot.name
    image = spot.imageName
    description = spot.desc
    latitude = spot.latitude
    longitude = spot.longitude


    pageContent = {'file_path' : image,
                   'spot_name' : spot_name,
                   'spot_description': description,
                   'spot_latitude': latitude,
                   'spot_longitude': longitude}


    return render(request, 'home.html', pageContent)
