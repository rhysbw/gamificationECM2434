from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.db.models import Q
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordResetForm

from .forms import SignupForm, ProfilePictureForm
from .models import Spot, UserInfo, SpotRecord, Avatar, UserRegister
import random
from user_agents import parse
import datetime
from .extra import extra_dictionary

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
                try:
                    userinfo = UserInfo.objects.create(
                        user=user_account,  # Links new user to new data in UserInfo
                        title='Sapling',  # Placeholder default title
                        avatarId=Avatar.objects.get(avatarTitle='Emotionless Default')
                    )
                    # Saves the record into the table
                    userinfo.save()
                except:
                    Avatar.objects.create(
                        imageName='https://i.imgur.com/fhrZmo9.png',
                        avatarTitle='Emotionless Default'
                    )
                    UserInfo.objects.create(
                        user=user_account,  # Links new user to new data in UserInfo
                        title='Sapling',  # Placeholder default title
                        avatarId=Avatar.objects.get(avatarTitle='Emotionless Default')
                    )

                    pass
            except:
                # Here a fail would only a occur if there was that user was already in UserInfo
                pass
            user = authenticate(username=account_username, password=raw_password)
            login(request, user)
            return redirect('pledge')
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


@login_required()
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


@login_required()
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


@login_required()
def home_page(request):
    """
    This view facilitates the display of the profile page at exseed.duckdns.org/
    param: request (HTTP_REQUEST): The Django-supplied web request that contains information about the current request to see this view
    returns:
        PAGE_REDIRECT: If certain criteria are not met (user is logged in, user is on mobile device), the view returns a redirect to the
        appropriate page to handle this
        Non-erroneous return: (request, 'profile.html', page_contents)
        request (HTTP_REQUEST): Passes on request data to the webpage
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

    if not request.user.is_superuser:
        if not UserInfo.objects.get(user__pk=request.user.pk).hasTakenPledge:
            return redirect('/pledge')
    # Find the date of today
    today = datetime.date.today()

    # Checks if there is a spot for today and if not a new one will be assigned
    try:
        spot = SpotRecord.objects.get(spotDay=today).sId
    except:
        # This clause is entered when there is no spot set to today
        yesterday = today - datetime.timedelta(days=1)
        # Continuously checks for a new spot until it finds one that is not the same as yesterdays
        while True:
            # pick a random spot
            spot = random.choice(Spot.objects.all())
            # check if that is the same as yesterday and if so get a new one
            try:
                if spot.pk != SpotRecord.objects.get(spotDay=yesterday).sId.pk:
                    break
            except:
                # This case is entered when there is no spot assigned to yesterday
                # In this case, there is no concern for picking yesterday's spot, since it doesn't exist
                break
        # Assigns the new spot of the day as the new chosen one
        SpotRecord(sId=spot, spotDay=today).save()

        # ADD STREAK STUFF HERE
        '''
        yesterdaysRegister = UserInfo.objects.filter(~Q(lastSpotRegister=yesterday))
        yesterdaysRegister.update(currentStreak=0)
        for item in yesterdaysRegister:
            item.save()
        '''
    # Assigns the values of today's spot so they can be rendered into the website
    spot_name = spot.name
    image = spot.imageName
    description = spot.desc
    latitude = spot.latitude
    longitude = spot.longitude
    average_stars, background_colours = graph()
    fact = random.choice(extra_dictionary['facts'])

    page_contents = {'file_path': image,
                     'spot_name': spot_name,
                     'spot_description': description,
                     'spot_latitude': latitude,
                     'spot_longitude': longitude,
                     "spot_data": average_stars,
                     "colours": background_colours,
                     "fact": fact
                     }

    return render(request, 'home.html', page_contents)


@login_required()
def leaderboard(request):
    """This view facilitates the display of the leaderboard at exseed.duckdns.org/leaderboard

    Args: request (HTTP_REQUEST): The Django-supplied web request that contains information about the current request
    to see this view

    Returns:
        PAGE_REDIRECT: If certain criteria are not met (user is logged in, user is on mobile device), the view returns a
            redirect to the appropriate page to handle this
        Non-erroneous return: (request, 'leaderboard.html', page_contents)
        request (HTTP_REQUEST): Passes on request data to the webpage
        'leaderboard.html' (str): The string name of the desired html doc the page_contents should be displayed on
        page_contents (library): A library of information to be displayed on the leaderboard webpage
            new_leaderboard_data ([rank,score,pfp,name,title]): Contains user data to go on leaderboard
            lb_type (str): Tells the webpage which type of leaderboard is being rendered

    @author: Rowan N
    """
    # Checks if the user is on a desktop instead of mobile and if
    # so renders the QR code page
    user_agent = parse(request.META['HTTP_USER_AGENT'])
    if not user_agent.is_mobile:
        return render(request, 'QRCodePage.html')

    if not request.user.is_superuser:
        if not UserInfo.objects.get(user__pk=request.user.pk).hasTakenPledge:
            return redirect('/pledge')

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
    additional_rankings = []  # Holds additional rankings needed (when user is below top 5)
    new_leaderboard_data = []
    above_name = None

    # If the user is within the top 5, only the top 5 need be shown
    for record in top_rankings:
        position, buffer = position_buffer_calc(position, buffer, record, column_name, prev_position_score)
        if user == record.user.pk:
            user_in_top_five = True  # User found in top 5, so no additional_rankings required
            user_position = position + buffer  # The users index in the ordered table
        prev_position_score = getattr(record, column_name)  # Saves previous rank's score
        new_leaderboard_data.append([position, prev_position_score, record.avatarId.imageName, record.user.username, record.title])

    # Elif the user is within the top 7, gather only their record and any above (so if 6, get only 6)
    if not user_in_top_five:
        six_and_seven = UserInfo.objects.order_by(sort_column, other)[5:7]  # The database records for users in
        # positions 6 and 7
        for record in six_and_seven:
            position, buffer = position_buffer_calc(position, buffer, record, column_name, prev_position_score)
            additional_rankings.append([position, getattr(record, column_name), record.avatarId.imageName, record.user.username, record.title])
            if user == record.user.pk:
                user_in_top_seven = True
                user_position = position + buffer
                for item in additional_rankings:
                    new_leaderboard_data.append(item)
                break  # Once user is found, no additional information is needed, and thus we break out of the loop
            prev_position_score = getattr(record, column_name)  # Saves previous rank's score

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
                    above_name = record.user.username
                elif counter == 0 or counter == 1:
                    position, buffer = position_buffer_calc(position, buffer, record, column_name, prev_position_score)
                    # Evaluates user and one below
                prev_position_score = getattr(record, column_name)
                additional_rankings.append([position, getattr(record, column_name), record.avatarId.imageName, record.user.username, record.title])  # Rank and record appended to 2D array
                counter += 1  # Increments counter so the program knows which record it is looking at
            for item in additional_rankings:
                new_leaderboard_data.append(item)

    # If any of these states are true, dots are not needed in the leaderboard. This data is passed to the html 
    #no_dots = user_in_top_five or user_in_top_seven or user_position is None
    # Library for all data needed in the leaderboard
    pageContent = {
        'leaderboardType': lb_type,
        'UserResults': new_leaderboard_data,
        'above_name': above_name
    }

    return render(request, 'leaderboard.html', pageContent)


@login_required()
def profile_page(request):
    """This view facilitates the display of the leaderboard at exseed.duckdns.org/profile
    Args:
        request (HTTP_REQUEST): The Django-supplied web request that contains information about the current request to see this view

    Returns:
        PAGE_REDIRECT: If certain criteria are not met (user is logged in, user is on mobile device), the view returns a redirect to the
        appropriate page to handle this
        Non-erroneous return: (request, 'profile.html', page_contents)
        request (HTTP_REQUEST): Passes on request data to the webpage
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

    try:
        if not UserInfo.objects.get(user__pk=request.user.pk).hasTakenPledge:
            return redirect('/pledge')
    except:
        return render(request, 'adminInfo.html')

    # Takes the users information from the user and UserInfo table to be assigned to the page_contents variables.
    user = request.user.pk
    user_info = UserInfo.objects.filter(user_id=user).values()
    streak = user_info[0]['currentStreak']
    title = user_info[0]['title']
    totalScore = user_info[0]['totalPoints']
    profile_id = user_info[0]['avatarId_id']
    profile_image = Avatar.objects.get(id=profile_id).imageName
    all_avatars_ref = Avatar.objects.values_list('imageName')
    all_avatars = list(all_avatars_ref)

    streak_image = get_streak_image(user, 'profile')
    page_contents = {
        "streak": streak,
        "total" : totalScore,
        "title": title,
        "titles": extra_dictionary['titles'],
        "profileImage": profile_image,
        "avatars": all_avatars,
        "streak_image": streak_image
    }
    return render(request, 'profile.html', page_contents)


def graph() -> tuple[list[int],list[str]]:
    """This function gathers all of todays spot's ratings, finds the average for each hour and puts all the data into an
        array for the graph. It also supplies the appropriate bar colour for each hour on the graph.

    Returns:
        tuple[list[int],list[str]]: A tuple containing the list of average spot score (int) and their corresponding colours (str)

    @author Rowan N
    """
    # Gather all of today's star ratings
    spot_data = UserRegister.objects.filter(srId__spotDay=datetime.date.today()).order_by('registerTime')
    # If empty graph not wanted to be viewed, here is where we could check if spot_data had any contents and redirect
    # Array of all average values where index 0 = 9:00 and index 7 is 16:00
    average_stars = [0, 0, 0, 0, 0, 0, 0, 0]
    previous_hour = -1
    hour_total = 0
    records_in_hour = 0
    for record in spot_data:
        hour = record.registerTime.hour
        if hour == previous_hour or previous_hour == -1:  # If the previous_hour is -1 then this is the first record
            # If hour == previous_hour, then we are still getting details from the same hour, and so totals should be added to
            hour_total += record.spotNiceness 
            records_in_hour += 1
        else:  # We arrive here when we are dealing with a different time to the previous record
            average_stars[previous_hour - 9] = float(hour_total) / records_in_hour  # Last hours details are saved
            hour_total = record.spotNiceness # hour_total and records_in_hour are reset for new hour
            records_in_hour = 1
        previous_hour = hour # Ensures we're always looking at the most recent hour
    try:
        average_stars[previous_hour - 9] = float(hour_total) / records_in_hour  # Makes sure the final value is added
    except IndexError:
        pass  # Avoids previous_hour calling an index that is not present (aka -7)
    except ZeroDivisionError:
        pass  # Avoids zero division when no records are returned to spot_data

    background_colours = [] # Will store the colours for each bar
    for item in average_stars:
        if item <= 1:
            background_colours.append("rgb(237,28,36)")  # Worst
        elif item <= 2:
            background_colours.append("rgb(255,163,100)")  # Bad
        elif item <= 3:
            background_colours.append("rgb(255,201,14)")  # Middle
        elif item <= 4:
            background_colours.append("rgb(182,230,32)")  # Good
        else:
            background_colours.append("rgb(34,177,76)")  # Great


    return average_stars, background_colours


@login_required()
def compass(request):
    user_agent = parse(request.META['HTTP_USER_AGENT'])
    if not user_agent.is_mobile:
        return render(request, 'QRCodePage.html')

    # Checks if the user is logged in or not, if not they are automatically redirected
    # to the login page

    if not request.user.is_superuser:
        if not UserInfo.objects.get(user__pk=request.user.pk).hasTakenPledge:
            return redirect('/pledge')

    # Find the date of today
    today = datetime.date.today()

    # Checks if there is a spot for today and if not returns the user to the home page (where one will be assigned)
    try:
        spot = SpotRecord.objects.filter(spotDay=today).first().sId
    except:
        return redirect('/')

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


@login_required()
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



    if request.method == "POST":
        chosen_pfp = request.POST.get('chosen_pfp')
    user = request.user.pk

    # Edits the user_info table to add the id of the new profile picture
    try:
        to_edit = UserInfo.objects.get(user_id=user)
        new_avatar = Avatar.objects.get(imageName=chosen_pfp)
        to_edit.avatarId_id = new_avatar.id
        to_edit.save()
    except:
        pass

    return redirect('/profile')


@login_required()
def addScore(request):
    """Adds score and streak to a user once they arrive at the spot. Also logs this users rating of the spot.
        This view also implements streak resetting for users who did not attend the spot yesterday, and calculates yesterday's spots new spot average

    Args:
        request (HTTP_request): The Django-supplied web request that contains information about the current request to see this view

    Returns:
        Erroneous-returns: Ensures users who get to this url in an undesired manner are redirected to avoid errors
            Non-mobile users are redirected to the 'You cannot access this resource on a non-mobile device' page
            Users who aren't logged in are redirected to log in
            Users who got here without a POST http_request are redirected to home.html
            Users who are registering at an incorrect time are redirected to error.html, where their mistake is displayed
            Users who have already registered are redirected to error.html, where their mistake is displayed
        Non-erroneous return: Returns the user to home.html once they've been successfully registered

    @author Rowan N
    """
    
    # Checks if the user is on a desktop instead of mobile and if
    # so renders the QR code page
    user_agent = parse(request.META['HTTP_USER_AGENT'])
    if not user_agent.is_mobile:
        return render(request, 'QRCodePage.html')
    
    # Ensures a user who did not get here by sending a post request from home.html gets redirected back home
    if request.method == "POST":
        user_spot_rating = int(request.POST.get('star'))
    else:
        redirect('/')

    today = datetime.date.today()
    first_register = UserInfo.objects.filter(lastSpotRegister=today)

    # If the user is the first person to add a score
    if len(first_register) == 0:
        yesterday = today - datetime.timedelta(days=1)
        # Gets ALL UserInfo records that have not played either yesterday or today
        # Today is only included in case of errors, there should never actually be any users that registered today
        yesterdaysRegister = UserInfo.objects.filter(~Q(lastSpotRegister=yesterday) & ~Q(lastSpotRegister=today))
        yesterdaysRegister.update(currentStreak=0)  # Makes all their streaks 0
        for item in yesterdaysRegister:
            item.save()  # Saves each item. No bulk saving method

        # This code works out the average spot attendance value
        prev_spot = SpotRecord.objects.get(spotDay=yesterday) # Finds the spot that was SotD yesterday
        total_spot_times = len(SpotRecord.objects.filter(sId=prev_spot.sId)) # How many times has this spot been spot of the day
        spot = Spot.objects.get(pk=prev_spot.sId.pk)
        if total_spot_times == 1: # If there has only been one spot instance for this spot, then the average is yesterdays attendance
            spot.average_attendance = prev_spot.attendance
        else: # The spot has been SotD multiple times
            total_attendance = spot.average_attendance * (total_spot_times - 1) # 'Reverses' average to find a rough total attendance
            total_attendance += prev_spot.attendance
            spot.average_attendance = total_attendance / total_spot_times # Updates average with latest attendance
            # NOTE: This system isn't the most accurate, as we could go through all spot instances to get an exact average, however
            # this felt like an unnecessary computation when the above system does the same thing with minimal accuracy loss
        spot.save() # Saves the new spot data

    now = datetime.datetime.now()
    nowTime = now.time()
    #nowTime = datetime.time(12,12,12)  # Used only for the purpose of testing outside of allowed times (6am to 7pm)

    if nowTime.hour < 9 or nowTime.hour > 16: # Ensures that the user cannot register outside of accepted times
        return render(request, 'error.html', {'error': 'time'}) # Informs the user of their error

    # Checks if there is a spot for today and if not returns the user to the home page (where one will be assigned)
    try:
        spot = SpotRecord.objects.get(spotDay=today)
    except:
        return redirect('/')

    try:
        register = UserRegister.objects.get(uId=request.user, srId=spot)
        # If there is no error in fetching this record then the current user has already registered
    except  :
        # Adds their score to the database
        todays_registers = UserInfo.objects.filter(lastSpotRegister=today)
        # Additional points are given to the earliest 4 users. First gets 5 total points, second 4, third 3, fourth 2
        additional_points = 4 - len(todays_registers)
        if additional_points < 0:
            additional_points = 0 # This ensures that later users do not get negative points
        info = UserInfo.objects.get(user_id=request.user.pk)

        info.totalPoints = info.totalPoints + 1 + additional_points
        info.currentStreak = info.currentStreak + 1
        info.lastSpotRegister = today

        spot.attendance = spot.attendance + 1
        UserRegister(uId=request.user, srId=spot, spotNiceness=user_spot_rating, registerTimeEditable=nowTime).save() # Registers user at spot
        spot.save() # Saves spot with incremented attendance
        info.save() # Saves the new lastSpotRegister for the user
        return redirect('/') # Returns the user home

    return render(request, 'error.html', {'error': 'already'}) # Ensures the user can only register once


@login_required()
def change_title(request, title):
    """
    Changes the users title based on their input
    param: request
    """
    user_agent = parse(request.META['HTTP_USER_AGENT'])
    if not user_agent.is_mobile:
        return render(request, 'QRCodePage.html')

    info = UserInfo.objects.get(user_id=request.user.pk)
    info.title = title
    info.save()
    return redirect('/profile')


@login_required()
def pledge(request):
    """Renders the pledge to a user once they've registered/when they try to access pages having not accepted the pledge

    Args:
        request (HTTP_request): The Django-supplied web request that contains information about the current request to see this view

    Returns:
        request (HTTP_REQUEST): Passes on request data to the webpage
        'pledge.html' (str): The string name of the desired html doc to show the user

    @author Rowan N
    """
    return render(request, 'pledge.html')


@login_required()
def take_pledge(request):
    """Records that this user has taken the SotD pledge

    Args:
        request (HTTP_request): The Django-supplied web request that contains information about the current request to see this view

    Returns:
        Sends the user to the home page

    @author Rowan N
    """
    if request.method == "POST": # Only takes action when the user gets where with a POST request
        info = UserInfo.objects.get(user__pk=request.user.pk)
        info.hasTakenPledge = True
        info.save() # Saves the UserInfo to record they've taken the pledge
    return redirect('/')


def position_buffer_calc(position, buffer, record, column_name, prev_pos_score) -> tuple[int,int]:  # FUNCTION
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


def get_streak_image(user_pk, imageType) -> str: # FUNCTION
    """Returns the relevant streak image for a given user, such that every view can access them

    Args:
        user_pk (int): The current users assigned primary key (accessible through request.user.pk)
        imageType (str): Defines which kind of streak image is returned. Can be "profile" or "leaderboard"
            NOTE: Leaderboard streak images phased out of deployment product

    Returns:
        str: The link to the desired image that represents the current users active streak

    @author Rowan N
    """
    user = UserInfo.objects.get(user__pk=user_pk)


    pictures = [
        "https://i.imgur.com/V0r8Ftw.png",  # stage one
        "https://i.imgur.com/9VZtO9X.png",  # stage two
        "https://i.imgur.com/3zJQoI3.png",  # stage three
        "https://i.imgur.com/pweVVh2.png",  # stage four
        "https://i.imgur.com/6jzElXg.png",  # stage five
        "https://i.imgur.com/nHUmeOw.png",  # stage six
        "https://i.imgur.com/Yg5CGvc.png",  # stage seven
        "https://i.imgur.com/BCPvB1V.png",  # stage eight
        "https://i.imgur.com/8FxfFdV.png",  # stage nine
        "https://i.imgur.com/WS9jEuH.png",  # stage ten
        "https://i.imgur.com/IgO05pc.png",  # stage eleven
        "https://i.imgur.com/d1Jz3G8.png"  # stage twelve +
    ]
    streak = user.currentStreak
    # Ensures streak cannot go above 5 or below 1 (to fit image constraints)
    if streak > 11:
        streak = 12
    elif streak == 0:
        streak = 1


    return pictures[streak - 1]


def privacy_policy(request):
    """
    :param request:
    :return:
    @author Sam Tebbet
    """
    return render(request, 'privacy_policy.html')



