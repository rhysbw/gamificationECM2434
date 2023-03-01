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


def position_buffer_calc(position, buffer, record, column_name, prev_pos_score):
    """Determines if there are any repeated score values that deserve repeated ranks

    Args:
        position (int): The current position being evaluated
        buffer (int): The buffer int, allowing ranks to be skipped in the presence of repeated score
        record (QuerySet): The current position's QuerySet
        column_name (str): Name of the column being ranked
        prev_pos_score(int): The score of the previous record

    Returns:
        (int, int): The position and buffer values
        
    @author = Rowan N
    """
    new_pos = position  # New position
    new_buf = buffer  # New buffer
    if prev_pos_score is None:  # This means this is the first record (and thus no comparison is needed)
        pass
    elif prev_pos_score == getattr(record, column_name):  # If scores are the same, position should stay the same
        new_buf += 1  # The buffer increments to make up for the skipped position
    else:  # The values are NOT equal, and as such the rank must increase
        new_pos += buffer
        new_buf = 1 
    return new_pos, new_buf  # Gives the new position and buffer values back to the main code

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
    """This view facilitates the display of the leaderboard at exseed.duckdns.org/leaderboard

    Args:
        request (HTML_REQUEST): The Django-supplied web request that contains information about the current request to see this view

    Returns:
        PAGE_REDIRECT: If certain criteria are not met (user is logged in, user is on mobile device), the view returns a redirect to the
        appropriate page to handle this
        Non-erroneous return: (request, 'leaderboard.html', page_contents)
        request (HTML_REQUEST): Passes on request data to the webpage
        'leaderboard.html' (str): The string name of the desired html doc the page_contents should be displayed on
        page_contents (library): A library of information to be displayed on the leaderboard webpage
            rank_and_rec ([int, Query]): Contains users rank and corresponding database record
            user (int): The current user's primary key value (UserID)
            no_dots (bool): Defines whether a leaderboard will require a dots line (for when the user is significantly below the top)
            additional_rankings ([int, Query]): A 2D array containing additional data (for when the user is below the top 5)
            user_position (int): The current user's position within the leaderboard
    """
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
    # The 'other' variable ensures that records are ordered by the not-selected score after initial ordering
    # sp that tying users are represented in order of the other attribute (seemed fair)
    lb_type = request.GET.get('q', '')
    sort_column, other = "", ""
    if lb_type == "streak":
        sort_column = "-currentStreak"
        other = "-totalPoints"
    elif lb_type == "total":
        sort_column = "-totalPoints"
        other = "-currentStreak"
    else:
        return redirect('/leaderboard?q=streak')  # If this is reached, the url includes a value not recognised, and as such
                                                  # has redirected to a valid url value (the streak leaderboard)

    # This block contains all required data to process, refine and display leaderboard data
    user = request.user.pk  # Gets the current users user id
    top_rankings = UserInfo.objects.order_by(sort_column, other)[:5]  # Top 5 users
    user_in_top_five = False  # If user is in top five, only top five should be shown
    user_in_top_seven = False  # If the user is in the top seven, then there needn't be a '...' and then their position
    user_position = None  # Keeps track of current user's position on the table. This is NOT the user's rank on said table
    position = 1  # Keeps track of current records rank
    prev_position_score = None  # Keeps track of the previous record's score for sake of repeated positions
    prev_prev_position_score = None  # Required for when user is below the top 7 (to accurately judge the record above the user)
    column_name = sort_column[1:]  # Removes '-' from column name so that it can be used in conjunction with getattr()
    buffer = 1  # Handles repeated positions
    rank_and_rec = []  # Lines up record with their position(aka rank) on the leaderboard
    additional_rankings = []  # Holds additional rankings needed (when user is below top 5)

    # If the user is within the top 5, only the top 5 need be shown
    for record in top_rankings:
        position, buffer = position_buffer_calc(position, buffer, record, column_name, prev_position_score)
        RaR = [position, record]  # short for rank_and_record, an array to be appended to the 2D rank_and_rec array
        rank_and_rec.append(RaR)  # Adds the Query and it's correct position to the rankings
        if user == record.user.pk:
            user_in_top_five = True  # User found in top 5, so no additional_rankings required
            user_position = position + buffer  # The users index in the ordered table
        prev_position_score = getattr(record, column_name)  # Saves prevous rank's score

    # Elif the user is within the top 7, gather only their record and any above (so if 6, get only 6)
    if not user_in_top_five:
        six_and_seven = UserInfo.objects.order_by(sort_column, other)[5:7]  # The database records for users in positions 6 and 7
        for record in six_and_seven:
            position, buffer = position_buffer_calc(position, buffer, record, column_name, prev_position_score)
            RaR = [position, record]
            additional_rankings.append(RaR)
            if user == record.user.pk:
                user_in_top_seven = True
                user_position = position + buffer
                break  # Once user is found, no additional information is needed, and thus we break out of the loop
            prev_position_score = getattr(record, column_name)  # Saves prevous rank's score

    # Else, get the user's record, and their neighbours (one above, one below)
    if not user_in_top_seven and not user_in_top_five:
        additional_rankings = []  # Clears any additional data recorded during six_and_seven analysis
        remainder = UserInfo.objects.order_by(sort_column, other)[7:]  # The rest of the database to search through
        prev_buf = None  # Keeps track of the previous buffer (used when reverting to a previous state once user is found)
        for record in remainder:
            if user == record.user.pk:  # User has been found. Record their place in the table to get records above and below
                user_position = position + buffer
                break
            prev_buf = buffer
            position, buffer = position_buffer_calc(position, buffer, record, column_name, prev_position_score)
            prev_prev_position_score = prev_position_score
            prev_position_score = getattr(record, column_name)  # Saves the score of the record two iterations ago (used when reverting to previous state once user found)

        # By this point, if user_position doesn't exist, the user is NOT in the UserInfo table!!!
        if user_position is not None:  # This avoids errors if the user doesn't have a UserInfo entry (WHICH SHOULDN'T BE EXPERIENCED)
            adjacent = UserInfo.objects.order_by(sort_column, other)[user_position-2:user_position+1]
            # Since we have found the user, we are now going BACK a step to evaluate the rank above the user. As such we need to revert the
            # position/buffer state to how it was when evaluating the record above the user
            if prev_buf is None:  # This means the user is in eighth place, and thus no action need be taken
                pass
            elif buffer == 1:  # This means the previous action did NOT increment the buffer (previous position/buffer state needed)
                buffer = prev_buf
                position -= buffer
            else:  # If the buffer isn't 1, then the previous pos_buf_calc's action was to increment the buffer, and as such we can simply revert
                   # this action to go back to the previous position/buffer state
                buffer -= 1
            counter = -1  # Counts which record we are looking at (-1 is above user, 0 is user, 1 is below user)
            for record in adjacent:
                if counter == -1:
                    position, buffer = position_buffer_calc(position, buffer, record, column_name,
                                                            prev_prev_position_score)  # Re-evaluates record above user
                elif counter == 0 or counter == 1:
                    position, buffer = position_buffer_calc(position, buffer, record, column_name, prev_position_score)  # Evaluates user and one below
                prev_position_score = getattr(record, column_name)
                RaR = [position, record]  # Rank and record saved in correct format
                additional_rankings.append(RaR)  # Rank and record appended to 2D array
                counter += 1  # Increments counter so the program knows which record it is looking at

    # If any of these states are true, dots are not needed in the leaderboard. This data is passed to the html 
    no_dots = user_in_top_five or user_in_top_seven or user_position is None
    # Library for all data needed in the leaderboard
    pageContent = {'rankings': rank_and_rec, 'currentUser': user, 'noDots': no_dots,
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

    user = request.user.pk
    userinfo = UserInfo.objects.filter(user_id=user).values()
    streak = userinfo[0]['currentStreak']
    content = {
        "streak": streak,
        "profileImage": "https://i.imgur.com/QP8EIWK.png"
    }
    return render(request, 'profile.html', content)

def test(request):

    content = {'lat': 50.724864,
               'long': -3.5127296
               }
    return render(request, 'testPage.html', content)