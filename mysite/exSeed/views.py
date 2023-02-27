from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required

from .forms import SignupForm
from .models import Spot, UserInfo
import random
import re

from user_agents import parse

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

def get_random_spot():
    spots = Spot.objects.all()
    return random.choice(spots)


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

    filePaths = [
        "https://i.imgur.com/zxC3CwO.jpg", # Back of XFI
        "https://i.imgur.com/giM0n6t.jpg", # Community Garden
        "https://i.imgur.com/jkZ7csT.jpg", # East Park Pond
        "https://i.imgur.com/u7yqGqI.jpeg", #Duck pond
        "https://i.imgur.com/4Okic8y.jpg", #Reed hall orchid
        "https://i.imgur.com/iulNkYN.jpg", #Rock Garden
        "https://i.imgur.com/cE7q7ZL.jpg", #Stream
        "https://i.imgur.com/74XNFNu.jpg" #Valley of peace
                ]

    spot = get_random_spot()
    spot_name = spot.name
    image = filePaths[1]
    # image = filePaths[spot.imageName]

    pageContent = {'file_path' : image,
                   'spot_name' : spot_name}


    return render(request, 'home.html', pageContent)

def leaderboard(request):
    user_agent = parse(request.META['HTTP_USER_AGENT'])
    if not user_agent.is_mobile:  # Ensures the user is on mobile (users not allowed to access site on anything else)
        return render(request, 'QRCodePage.html')

    if not request.user.is_authenticated:  # Ensures user is logged in (this shouldn't be accessible if not)
        return redirect('/login')

    # All unapologetically robbed from above

    # This block determines which sort of leaderboard is desired (streak or overall points)
    url = request.get_full_path()
    streak_lb = re.search("streak$", url)
    sort_column = ""
    if streak_lb:
        sort_column = "-currentStreak"
    else:
        sort_column = "-totalPoints"

    user = request.user.pk  # Gets the current users user id
    top_sev_users = UserInfo.objects.order_by(sort_column)[:7]  # First 7 users
    top_rankings = UserInfo.objects.order_by(sort_column)[:5]  # Top 5 users
    user_in_top_seven = False  # If the user is in the top seven, then there needn't be a '...' and then their position
    user_position = 1
    for record in top_sev_users:
        if user == record.user.pk:
            user_in_top_seven = True
            additional_rankings = UserInfo.objects.order_by(sort_column)[5:7]
            break
        user_position += 1

    if not user_in_top_seven:
        remaining_users = UserInfo.objects.order_by(sort_column)[8:]
        for record in remaining_users:
            if user == record.user.pk:
                break
            user_position += 1
        additional_rankings = UserInfo.objects.order_by(sort_column)[user_position-1:user_position+1]

    pageContent = {'rankings': top_rankings, 'currentUser': user, 'UiTS': user_in_top_seven,
                   'extra': additional_rankings, 'position': user_position}
    
    return render(request, 'leaderboard.html', pageContent)
