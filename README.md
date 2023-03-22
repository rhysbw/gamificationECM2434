# [exSeed](https://exseed.duckdns.org) - Spot of the Day
- This is the repository for the Group Software Engineering Project for Group 18.
-  The project is a Web App running on the Django platform.
-  The aim of exSeed is to promote sustainability on the campus of the University of Exeter via the mean of gamification.
- Our app allows for users to be shown a 'Spot of the day' and try to gain a streak of visiting green/outdoor spaces, the app uses a users GeoLocation via their web browser to check they have reached the location

## Access
The site requires GPS location thus to have full access to the site one must use a mobile device (Chrome and Safari Tested) and is accessible at:
> https://exseed.duckdns.org
#### Users
1. User will be prompted to sign up for an account
2. Once logged in they will be shown the 'Spot of the day' and be given a method to find locate it
3. If a user is in the 'Spot of the day' they can press the "I'm Here" button and they application will award point once verified

Also can view:
- Leaderboard
- Profile Page

## Developer Info (Unix Based CLI Instructions)
The main site must be accessed via a mobile device, to do this from a PC please use Google Chrome in Developer mode and select mobile device. 
### Local Work
Please work from the Development Branch, and once feature complete merge into Deployment. <br>
To run the server locally:
1. Enter Virtual Environment - [Instructions](https://python.land/virtual-environments/virtualenv)
2. Enter base directory (../gamificationECM2434)
3. `pip install -r requirements.txt`
4. `cd mysite`
5. `python manage.py runserver 0.0.0.0:80`
6. Accessible at http://localhost/
All features are not available when locally hosting, as to retrieve the orientation and geolocation data you must have an active SSL certificate.
### Deployment Work
The site is hosted on a server accessible via SSH (connection details in secrets.txt). <br>
The server auto pulls from the Deployment Branch after a new push to that Branch. <br>
If there is if server is down a developer must SSH in and run the command `sudo systemctl restart apache2` <br>
Developers and gamekeepers can add spots to the Site from the admin page located at (login details in secrets.txt):
> https://exseed.duckdns.org/admin
### Testing
This project has built in testing methods to ensure the robustness of the code. These can be run via the following steps:
1. Enter Virtual Environment - [Instructions](https://python.land/virtual-environments/virtualenv)
2. Enter base directory (../gamificationECM2434)
3. `pip install -r requirements.txt`
4. `cd mysite`
5. `python manage.py test exSeed`


