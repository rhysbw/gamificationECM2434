from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.exceptions import ObjectDoesNotExist

from .forms import SignupForm
from .models import Spot, UserInfo, PreviousSpotAttend
import random
import re
from user_agents import parse
import datetime

# Create your views here.
def signup(request):
    # Checks if the user is on a desktop instead of mobile and if
    # so renders the QR code page
    user_agent = parse(request.META['HTTP_USER_AGENT'])
    if not user_agent.is_mobile:
        return render(request, 'QRCodePage.html')

    #Checks if user is logged in and if they are the user sent back to the home page
    if request.user.is_authenticated:
        return redirect('/')

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

    # Checks if user is logged in and if they are the user sent back to the home page
    if request.user.is_authenticated:
        return redirect('/')

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

def leaderboard(request):
    # Checks if the user is on a desktop instead of mobile and if
    # so renders the QR code page
    user_agent = parse(request.META['HTTP_USER_AGENT'])
    if not user_agent.is_mobile:
        return render(request, 'QRCodePage.html')

    # Checks if the user is logged in or not, if not they are automatically redirected
    # to the login page
    if not request.user.is_authenticated:
        return redirect('/login')

    # This block determines which sort of leaderboard is desired (streak or overall points)
    url = request.get_full_path()
    lb_type = request.GET.get('q', '')
    sort_column = ""
    if lb_type == "streak":
        sort_column = "-currentStreak"
    elif lb_type == "total":
        sort_column = "-totalPoints"
    else:
        return redirect('/leaderboard?q=streak')

    user = request.user.pk  # Gets the current users user id
    top_rankings = UserInfo.objects.order_by(sort_column)[:5]  # Top 5 users
    user_in_top_five = False  # If user is in top five, only top five should be shown
    user_in_top_seven = False  # If the user is in the top seven, then there needn't be a '...' and then their position
    user_position = None  # Keeps track of current user's position on the table
    position = 0  # Keeps track of current records position
    rank_and_no = []  # Lines up record with their position on the leaderboard
    additional_rankings = []  # Holds additional rankings needed

    # If the user is within the top 5, only the top 5 need be shown
    for record in top_rankings:
        position += 1
        RaN = [position, record]
        rank_and_no.append(RaN)
        if user == record.user.pk:
            user_in_top_five = True
            user_position = position

    # Elif the user is within the top 7, gather only their record and any above (so if 6, get only 6)
    if not user_in_top_five:
        six_and_seven = UserInfo.objects.order_by(sort_column)[5:7]
        for record in six_and_seven:
            position += 1
            RaN = [position, record]
            additional_rankings.append(RaN)
            if user == record.user.pk:
                user_in_top_seven = True
                user_position = position
                break

    # Else, get the user's record, and their neighbours (one above, one below)
    if not user_in_top_seven and not user_in_top_five:
        additional_rankings = []
        remainder = UserInfo.objects.order_by(sort_column)[7:]
        for record in remainder:
            position += 1
            if user == record.user.pk:
                user_position = position
                break
        adjacent = UserInfo.objects.order_by(sort_column)[user_position-2:user_position+1]
        j = -1
        for record in adjacent:
            RaN = [user_position + j, record]
            additional_rankings.append(RaN)
            j += 1

    no_dots = user_in_top_five or user_in_top_seven
    # Library for all data needed in the leaderboard
    pageContent = {'rankings': rank_and_no, 'currentUser': user, 'noDots': no_dots,
                   'extra': additional_rankings, 'position': user_position}

    return render(request, 'leaderboard.html', pageContent)

def profile_page(request):
    # Checks if the user is on a desktop instead of mobile and if
    # so renders the QR code page
    user_agent = parse(request.META['HTTP_USER_AGENT'])
    if not user_agent.is_mobile:
        return render(request, 'QRCodePage.html')

    # Checks if the user is logged in or not, if not they are automatically redirected
    # to the login page
    if not request.user.is_authenticated:
        return redirect('/login')

    content = {
        "username" : "",
        "streak": "",
        "email": "",
        "profileImage": "https://i.imgur.com/QP8EIWK.png"
    }


    return render(request, 'profile.html', content)

def test(request):
    return render(request, 'testPage.html')