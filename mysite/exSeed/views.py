from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required

from .forms import SignupForm, ProfilePictureForm
from .models import Spot, UserInfo, PreviousSpotAttend, Avatar
import random

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
    """
    View for '/signup': Registers a user in the django.contrib.auth user table
    :param request:
            The Django-supplied web request that contains information about the current request to see this view
    :return render()
            Redirects the user to '/' where they will be able to see the spot of the day
    @author: Sam Tebbet, Benjamin Pickup
    """
    # Checks if the user is on a desktop instead of mobile and if
    # so renders the QR code page
    user_agent = parse(request.META['HTTP_USER_AGENT'])
    if not user_agent.is_mobile:
        return render(request, 'QRCodePage.html')

    # Checks if user is logged in and if they are the user sent back to the home page
    if request.user.is_authenticated:
        return redirect('/')

    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            account_username = form.cleaned_data.get('username')
            account_email = form.cleaned_data.get('email')
            raw_password = form.cleaned_data.get('password1')

            # Create a record in additional user info as long as there isn't already a record then
            try:
                user_account = User.objects.get(username=account_username)
                # Fills the userInfo record with data
                userinfo = UserInfo.objects.create(
                    user=user_account,  # Links new user to new data in UserInfo
                    title='Sapling',  # Placeholder default title
                )
                # Saves the record into the table
                userinfo.save()
            except:
                # Here a fail would only a occur if there was that user was already in UserInfo
                pass

            user = authenticate(username=account_username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = SignupForm()
    return render(request, 'signup.html', {"register_form": form})


def login_request(request):
    """
    View for '/login': Logs a user in to the website if they have an account
    :param request:
            The Django-supplied web request that contains information about the current request to see this view
    :return render()
            Redirects the user to '/' where they will be able to see the spot of the day
    @author: Sam Tebbet
    """
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
    """
    View for '/logout': Logs the user out of the website
    :param request:
            The Django-supplied web request that contains information about the current request to see this view
    :return render()
            Redirects the user to '/' where they will be able to see the spot of the day
    @author: Sam Tebbet
    """
    logout(request)
    messages.info(request, "You have successfully logged out")
    return redirect('home')


def delete_request(request, username):
    """
    View for '/delete/<username>': Registers a user in the django.contrib.auth user table
    :param request:
            The Django-supplied web request that contains information about the current request to see this view
    :param username:
            Username of the user deleting their account
    :return redirect()
            Redirects the user to '/' where they will be able to see the spot of the day
    @author: Sam Tebbet
    """
    try:
        user = User.objects.get(username=username)
        user.delete()
    except Exception as e:
        messages.error(request, f"Failed to delete user: {e}")
    return redirect('home')


def home_page(request):
    """
    This view facilitates the display of the profile page at exseed.duckdns.org/
    param: request (HTML_REQUEST): The Django-supplied web request that contains information about the current request to see this view
    returns:
        PAGE_REDIRECT: If certain criteria are not met (user is logged in, user is on mobile device), the view returns a redirect to the
        appropriate page to handle this
        Non-erroneous return: (request, 'profile.html', page_contents)
        request (HTML_REQUEST): Passes on request data to the webpage
        'home.html' (str): The string name of the desired html doc the page_contents should be displayed on.
        page_contents (library): A library of information to be displayed on the profile webpage.
            image (str) : The url for the current spot of the day.
            description (str) : The description for the current spot of the day.
            latitude (int) : The latitude coordinate of the current spot of the day.
            longitude (int) : The longitude coordinate of the current spot of the day.

    @author: Benjamin & Sam Tebbet
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

    # Find the date of today
    today = datetime.date.today()

    # Checks if there is a spot for today and if not a new one will be assigned
    try:
        spot = PreviousSpotAttend.objects.filter(spotDay=today).first().sId
    except:
        yesterday = today - datetime.timedelta(days=1)
        # Continously keeps checking for a new spot until it finds one that is not the same as yesterdays
        while True:
            # pick a random spot
            spot = random.choice(Spot.objects.all())
            # check if that is the same as yesterday and if so get a new one
            try:
                if spot.id != PreviousSpotAttend.objects.filter(spotDay=yesterday)[0].sId:
                    False
            except:
                break
        # Assigns the new spot of the day as the new chosen one
        PreviousSpotAttend(sId=spot, attendance=0, spotDay=today).save()

    # Assigns the values of today's spot so they can be rendered into the website
    spot_name = spot.name
    image = spot.imageName
    description = spot.desc
    latitude = spot.latitude
    longitude = spot.longitude

    page_contents = {'file_path': image,
                     'spot_name': spot_name,
                     'spot_description': description,
                     'spot_latitude': latitude,
                     'spot_longitude': longitude}

    return render(request, 'home.html', page_contents)


def leaderboard(request):
    """This view facilitates the display of the leaderboard at exseed.duckdns.org/leaderboard

    Args: request (HTML_REQUEST): The Django-supplied web request that contains information about the current request
    to see this view

    Returns:
        PAGE_REDIRECT: If certain criteria are not met (user is logged in, user is on mobile device), the view returns a
            redirect to the appropriate page to handle this
        Non-erroneous return: (request, 'leaderboard.html', page_contents)
        request (HTML_REQUEST): Passes on request data to the webpage
        'leaderboard.html' (str): The string name of the desired html doc the page_contents should be displayed on
        page_contents (library): A library of information to be displayed on the leaderboard webpage
            rank_and_rec ([int, Query]): Contains users rank and corresponding database record
            user (int): The current user's primary key value (UserID)
            no_dots (bool): Defines whether a leaderboard will require a dots line (for when the user is significantly
                below the top)
            additional_rankings ([int, Query]): A 2D array containing additional data (for when the user is below top 5)
            user_position (int): The current user's position within the leaderboard

    @author: Rowan N
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
        return redirect('/leaderboard?q=streak')  # If this is reached, the url includes a value not recognised, and as
        # such has redirected to a valid url value (the streak leaderboard)

    # This block contains all required data to process, refine and display leaderboard data
    user = request.user.pk  # Gets the current users user id
    top_rankings = UserInfo.objects.order_by(sort_column, other)[:5]  # Top 5 users
    user_in_top_five = False  # If user is in top five, only top five should be shown
    user_in_top_seven = False  # If the user is in the top seven, then there needn't be a '...' and then their position
    user_position = None  # Keeps track of current user's position on the table. This is NOT the user rank on the table
    position = 1  # Keeps track of current records rank
    prev_position_score = None  # Keeps track of the previous record's score for sake of repeated positions
    prev_prev_position_score = None  # Required for when user is below the top 7 (to accurately judge the record
    # above the user)
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
        six_and_seven = UserInfo.objects.order_by(sort_column, other)[5:7]  # The database records for users in
        # positions 6 and 7
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
        prev_buf = None  # Keeps track of the previous buffer (used when reverting to a previous state once user found)
        for record in remainder:
            if user == record.user.pk:  # User has been found. Record their place in the table to get neighbour records
                user_position = position + buffer
                break
            prev_buf = buffer
            position, buffer = position_buffer_calc(position, buffer, record, column_name, prev_position_score)
            prev_prev_position_score = prev_position_score
            prev_position_score = getattr(record, column_name)  # Saves the score of the record two iterations ago (
            # used when reverting to previous state once user found)

        # By this point, if user_position doesn't exist, the user is NOT in the UserInfo table!!!
        if user_position is not None:  # This avoids errors if the user doesn't have a UserInfo entry (WHICH
            # SHOULD NEVER BE EXPERIENCED IF SIGNUP IMPLEMENTED AS REQUESTED)
            adjacent = UserInfo.objects.order_by(sort_column, other)[user_position - 2:user_position + 1]
            # Since we have found the user, we are now going BACK a step to evaluate the rank above the user. As such
            # we need to revert the position/buffer state to how it was when evaluating the record above the user
            if prev_buf is None:  # This means the user is in eighth place, and thus no action need be taken
                pass
            elif buffer == 1:  # This means the previous action did NOT increment the buffer (previous
                # position/buffer state needed)
                buffer = prev_buf
                position -= buffer
            else:  # If the buffer isn't 1, then the previous pos_buf_calc's action was to increment the buffer,
                # and as such we can simply revert this action to go back to the previous position/buffer state
                buffer -= 1
            counter = -1  # Counts which record we are looking at (-1 is above user, 0 is user, 1 is below user)
            for record in adjacent:
                if counter == -1:
                    position, buffer = position_buffer_calc(position, buffer, record, column_name,
                                                            prev_prev_position_score)  # Re-evaluates record above user
                elif counter == 0 or counter == 1:
                    position, buffer = position_buffer_calc(position, buffer, record, column_name, prev_position_score)
                    # Evaluates user and one below
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
    """This view facilitates the display of the leaderboard at exseed.duckdns.org/profile
    Args:
        request (HTML_REQUEST): The Django-supplied web request that contains information about the current request to see this view

    Returns:
        PAGE_REDIRECT: If certain criteria are not met (user is logged in, user is on mobile device), the view returns a redirect to the
        appropriate page to handle this
        Non-erroneous return: (request, 'profile.html', page_contents)
        request (HTML_REQUEST): Passes on request data to the webpage
        'profile.html' (str): The string name of the desired html doc the page_contents should be displayed on
        page_contents (library): A library of information to be displayed on the profile webpage
            streak (int) : The users current streak to be put into the html template
            title (str) : The users title
            profileImage (str) : The profile picture of the user to be displayed

    @author: Benjamin & Sam Tebbet
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

    # Takes the users information from the user and UserInfo table to be assigned to the page_contents variables.
    user = request.user.pk
    user_info = UserInfo.objects.filter(user_id=user).values()
    streak = user_info[0]['currentStreak']
    title = user_info[0]['title']
    profile_id = user_info[0]['avatarId_id']
    profile_image = Avatar.objects.get(imageName=profile_id).avatarTitle
    all_avatars_ref = Avatar.objects.values_list('avatarTitle')
    all_avatars = list(all_avatars_ref)
    page_contents = {
        "streak": streak,
        "title": title,
        "profileImage": profile_image,
        "avatars": all_avatars,
    }
    return render(request, 'profile.html', page_contents)


def compass(request):
    user_agent = parse(request.META['HTTP_USER_AGENT'])
    if not user_agent.is_mobile:
        return render(request, 'QRCodePage.html')

    # Checks if the user is logged in or not, if not they are automatically redirected
    # to the login page
    if not request.user.is_authenticated:
        return redirect('/login')

    # Find the date of today
    today = datetime.date.today()

    # Checks if there is a spot for today and if not a new one will be assigned
    try:
        spot = PreviousSpotAttend.objects.filter(spotDay=today).first().sId
    except:
        yesterday = today - datetime.timedelta(days=1)
        # Continously keeps checking for a new spot until it finds one that is not the same as yesterdays
        while True:
            # pick a random spot
            spot = random.choice(Spot.objects.all())
            # check if that is the same as yesterday and if so get a new one
            try:
                if spot.id != PreviousSpotAttend.objects.filter(spotDay=yesterday)[0].sId:
                    False
            except:
                break
        # Assigns the new spot of the day as the new chosen one
        PreviousSpotAttend(sId=spot, attendance=0, spotDay=today).save()

    # Assigns the values of today's spot so they can be rendered into the website
    spot_name = spot.name
    image = spot.imageName
    description = spot.desc
    latitude = spot.latitude
    longitude = spot.longitude

    page_contents = {
        'spot_lat': latitude,
        'spot_long': longitude}
    return render(request, 'compass.html', page_contents)
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream


def change_profile_picture(request):
    """
    :param request:
        The Django-supplied web request that contains information about the current request to see this view
    :return: redirect()
        Redirecting the user to /profile where they can see their updated profile picture

    @author: Sam Tebbet
    """
    user_agent = parse(request.META['HTTP_USER_AGENT'])
    if not user_agent.is_mobile:
        return render(request, 'QRCodePage.html')

    # Checks if the user is logged in or not, if not they are automatically redirected
    # to the login page
    if not request.user.is_authenticated:
        return redirect('/login')

    if request.method == "POST":
        chosen_pfp = request.POST.get('chosen_pfp')
    user = request.user.pk

    # Edits the user_info table to add the id of the new profile picture
    to_edit = UserInfo.objects.get(user_id=user)
    new_avatar = Avatar.objects.get(avatarTitle=chosen_pfp)
    to_edit.avatarId_id = new_avatar.imageName
    to_edit.save()

    return redirect('/profile')
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
