from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.shortcuts import render, redirect
from .forms import SignupForm
from django.contrib.auth.decorators import login_required
from exSeed.models import Spot
import random

# Create your views here.
def signup(request):
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
    # Checks if the user is logged in or not, if not they are automatically redirected
    # to the login page
    if not request.user.is_authenticated:
        return redirect('/login')

    filePaths = [
        "https://i.imgur.com/zxC3CwO.jpg",  # Back of XFI
        "https://i.imgur.com/giM0n6t.jpg",  # Community Garden
        "https://i.imgur.com/jkZ7csT.jpg",  # East Park Pond
        "https://i.imgur.com/u7yqGqI.jpeg", #Duck pond
        "https://i.imgur.com/4Okic8y.jpg", #Reed hall orchid
        "https://i.imgur.com/iulNkYN.jpg", #Rock Garden
        "https://i.imgur.com/cE7q7ZL.jpg", #Stream
        "https://i.imgur.com/74XNFNu.jpg" #Valley of peace
                ]

    spot = get_random_spot()
    spot_name = spot.name
    image = filePaths[spot.image_pointer - 1]

    pageContent = {'file_path' : image,
                   'spot_name' : spot_name}


    return render(request, 'home.html', pageContent)
