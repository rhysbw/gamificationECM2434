from django.contrib.auth.models import User
from django.test import TransactionTestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import UserInfo, Avatar, SpotRecord, Spot
import datetime

# Create your tests here.

class NonMobileTests(TransactionTestCase):

    def test_url(self):
        """
        Parameters:
            self

        Tests whether any page can be brought up by the url itself on a non-mobile device
        @author: Jonathan Tao
        """
        response = self.client.get('/signup', HTTP_USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36 Edg/91.0.864.59")
        self.assertEqual(response.status_code, 200) #test the status code returned
        self.assertTemplateUsed(response, template_name='QRCodePage.html') #test the template used. Since on a non-mobile device, the QR page template is used

    def test_url_via_name(self):
        """
        Parameters:
            self

        Tests whether any page can be brought up by the name associated with the url on a non-mobile device
        @author: Jonathan Tao
        """
        response = self.client.get(reverse('signup'), HTTP_USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36 Edg/91.0.864.59")
        self.assertEqual(response.status_code, 200)  # test the status code returned
        self.assertTemplateUsed(response, template_name='QRCodePage.html')  # test the template used. Since on a non-mobile device, the QR page template is used

class SignUpTests(TransactionTestCase):

    def test_url(self):
        """
        Parameters:
            self

        Tests whether the sign-up form can be brought up by the url itself
        @author: Jonathan Tao
        """
        response = self.client.get('/signup', HTTP_USER_AGENT = "Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_1 like Mac OS X) AppleWebKit/603.1.30 (KHTML, like Gecko) Version/10.0 Mobile/14E304 Safari/602.1")
        self.assertEqual(response.status_code, 200) #test the status code returned
        self.assertTemplateUsed(response, template_name='signup.html') #test the template used

    def test_url_via_name(self):
        """
        Parameters:
            self

        Tests whether the sign-up form can be brought up by the name associated with the url
        @author: Jonathan Tao
        """
        response = self.client.get(reverse('signup'), HTTP_USER_AGENT = "Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_1 like Mac OS X) AppleWebKit/603.1.30 (KHTML, like Gecko) Version/10.0 Mobile/14E304 Safari/602.1")
        self.assertEqual(response.status_code, 200) #test the status code returned
        self.assertTemplateUsed(response, template_name='signup.html') #test the template used

    def test_signup_form(self):
        """
        Parameters:
            self

        Tests the sign-up form
        @author: Jonathan Tao
        """
        response = self.client.post(reverse('signup'), HTTP_USER_AGENT = "Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_1 like Mac OS X) AppleWebKit/603.1.30 (KHTML, like Gecko) Version/10.0 Mobile/14E304 Safari/602.1", data={
            'username': 'testuser',
            'email': 'testuser@email.com',
            'password1': 'Hjguhjlkjbv765588',
            'password2': 'Hjguhjlkjbv765588'
        })  # create a request to sign-up as a user using the sign-up form
        users = get_user_model().objects.all()  # get all the users from the database
        self.assertEqual(response.status_code, 302)  # test the status code returned
        self.assertEqual(users.count(), 1)  # since this is the first user then there should only be 1 user

class LoginTests(TransactionTestCase):

    def test_url(self):
        """
        Parameters:
            self

        Tests whether the login form can be brought up by the url itself
        @author: Jonathan Tao
        """
        response = self.client.get('/login/', HTTP_USER_AGENT = "Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_1 like Mac OS X) AppleWebKit/603.1.30 (KHTML, like Gecko) Version/10.0 Mobile/14E304 Safari/602.1")
        self.assertEqual(response.status_code, 200) #test the status code returned
        self.assertTemplateUsed(response, template_name='registration/login.html') #test the template used

    def test_url_via_name(self):
        """
        Parameters:
            self

        Tests whether the login form can be brought up by the name associated with the url
        @author: Jonathan Tao
        """
        response = self.client.get(reverse('login'), HTTP_USER_AGENT = "Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_1 like Mac OS X) AppleWebKit/603.1.30 (KHTML, like Gecko) Version/10.0 Mobile/14E304 Safari/602.1")
        self.assertEqual(response.status_code, 200) #test the status code returned
        self.assertTemplateUsed(response, template_name='registration/login.html') #test the template used

    def test_login_form(self):
        """
        Parameters:
            self

        Tests the login form
        @author: Jonathan Tao
        """
        response = self.client.post(reverse('login'), HTTP_USER_AGENT = "Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_1 like Mac OS X) AppleWebKit/603.1.30 (KHTML, like Gecko) Version/10.0 Mobile/14E304 Safari/602.1", data={
            'username': 'testuser',
            'email': 'testuser@email.com',
            'password1': 'Hjguhjlkjbv765588'
        })  # create a request to login as a user using the login form
        self.assertEqual(response.status_code, 200)


class LogoutTests(TransactionTestCase):

    def test_url(self):
        """
        Parameters:
            self

        Tests whether the logout action can be performed by the url itself
        @author: Jonathan Tao
        """

        response = self.client.get('/logout', HTTP_USER_AGENT = "Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_1 like Mac OS X) AppleWebKit/603.1.30 (KHTML, like Gecko) Version/10.0 Mobile/14E304 Safari/602.1")
        self.assertEqual(response.status_code, 302) #test the status code returned. In this case since this webpage is accessed after login, there is a redirect and so 302 is returned

    def test_url_via_name(self):
        """
        Parameters:
            self

        Tests whether the logout action can be performed by the name associated with the url
        @author: Jonathan Tao
        """

        response = self.client.get(reverse('logout'), HTTP_USER_AGENT = "Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_1 like Mac OS X) AppleWebKit/603.1.30 (KHTML, like Gecko) Version/10.0 Mobile/14E304 Safari/602.1")
        self.assertEqual(response.status_code, 302) #test the status code returned. In this case since this webpage is accessed after login, there is a redirect and so 302 is returned

class HomeTests(TransactionTestCase):
    def test_url(self):
        """
        Parameters:
            self

        Tests whether the home page can be brought up by the url itself
        @author: Jonathan Tao
        """

        response = self.client.get('/', HTTP_USER_AGENT = "Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_1 like Mac OS X) AppleWebKit/603.1.30 (KHTML, like Gecko) Version/10.0 Mobile/14E304 Safari/602.1")
        self.assertEqual(response.status_code, 302) #test the status code returned. In this case since this webpage is accessed after login, there is a redirect and so 302 is returned

    def test_url_via_name(self):
        """
        Parameters:
            self

        Tests whether the home page can be brought up by the name associated with the url
        @author: Jonathan Tao
        """

        response = self.client.get(reverse('home'), HTTP_USER_AGENT = "Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_1 like Mac OS X) AppleWebKit/603.1.30 (KHTML, like Gecko) Version/10.0 Mobile/14E304 Safari/602.1")
        self.assertEqual(response.status_code, 302) #test the status code returned. In this case since this webpage is accessed after login, there is a redirect and so 302 is returned

class TestLeaderboard(TransactionTestCase):
    def test_url(self):
        """
        Parameters:
            self

        Tests whether the leaderboard can be brought up by the url itself
        @author: Jonathan Tao
        """

        response = self.client.get('/leaderboard', HTTP_USER_AGENT = "Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_1 like Mac OS X) AppleWebKit/603.1.30 (KHTML, like Gecko) Version/10.0 Mobile/14E304 Safari/602.1")
        self.assertEqual(response.status_code, 302) #test the status code returned. In this case since this webpage is accessed after login, there is a redirect and so 302 is returned

    def test_url_via_name(self):
        """
        Parameters:
            self

        Tests whether the leaderboard can be brought up by the name associated with the url
        @author: Jonathan Tao
        """

        response = self.client.get(reverse('leaderboard'), HTTP_USER_AGENT = "Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_1 like Mac OS X) AppleWebKit/603.1.30 (KHTML, like Gecko) Version/10.0 Mobile/14E304 Safari/602.1")
        self.assertEqual(response.status_code, 302) #test the status code returned. In this case since this webpage is accessed after login, there is a redirect and so 302 is returned

class TestProfilePage(TransactionTestCase):
    def test_url(self):
        """
        Parameters:
            self

        Tests whether the profile page can be brought up by the url itself
        @author: Jonathan Tao
        """

        response = self.client.get('/profile', HTTP_USER_AGENT = "Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_1 like Mac OS X) AppleWebKit/603.1.30 (KHTML, like Gecko) Version/10.0 Mobile/14E304 Safari/602.1")
        self.assertEqual(response.status_code, 302) #test the status code returned. In this case since this webpage is accessed after login, there is a redirect and so 302 is returned

    def test_url_via_name(self):
        """
        Parameters:
            self

        Tests whether the profile page can be brought up by the name associated with the url
        @author: Jonathan Tao
        """

        response = self.client.get(reverse('profile'), HTTP_USER_AGENT = "Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_1 like Mac OS X) AppleWebKit/603.1.30 (KHTML, like Gecko) Version/10.0 Mobile/14E304 Safari/602.1")
        self.assertEqual(response.status_code, 302) #test the status code returned. In this case since this webpage is accessed after login, there is a redirect and so 302 is returned

class TestCompass(TransactionTestCase):
    def test_url(self):
        """
        Parameters:
            self

        Tests whether the compass can be brought up by the url itself
        @author: Jonathan Tao
        """

        response = self.client.get('/compass', HTTP_USER_AGENT = "Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_1 like Mac OS X) AppleWebKit/603.1.30 (KHTML, like Gecko) Version/10.0 Mobile/14E304 Safari/602.1")
        self.assertEqual(response.status_code, 302) #test the status code returned. In this case since this webpage is accessed after login, there is a redirect and so 302 is returned

    def test_url_via_name(self):
        """
        Parameters:
            self

        Tests whether the compass can be brought up by the name associated with the url
        @author: Jonathan Tao
        """

        response = self.client.get(reverse('compass'), HTTP_USER_AGENT = "Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_1 like Mac OS X) AppleWebKit/603.1.30 (KHTML, like Gecko) Version/10.0 Mobile/14E304 Safari/602.1")
        self.assertEqual(response.status_code, 302) #test the status code returned. In this case since this webpage is accessed after login, there is a redirect and so 302 is returned

class TestChangeProfilePicturePage(TransactionTestCase):

    def test_url(self):
        """
        Parameters:
            self

        Tests whether the change profile picture page can be brought up by the url itself
        @author: Jonathan Tao
        """

        response = self.client.get('/change_profile_picture', HTTP_USER_AGENT = "Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_1 like Mac OS X) AppleWebKit/603.1.30 (KHTML, like Gecko) Version/10.0 Mobile/14E304 Safari/602.1")
        self.assertEqual(response.status_code, 302) #test the status code returned. In this case since this webpage is accessed after login, there is a redirect and so 302 is returned

    def test_url_via_name(self):
        """
        Parameters:
            self

        Tests whether the change profile picture page can be brought up by the name associated with the url
        @author: Jonathan Tao
        """

        response = self.client.get(reverse('change_profile_picture'), HTTP_USER_AGENT = "Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_1 like Mac OS X) AppleWebKit/603.1.30 (KHTML, like Gecko) Version/10.0 Mobile/14E304 Safari/602.1")
        self.assertEqual(response.status_code, 302) #test the status code returned. In this case since this webpage is accessed after login, there is a redirect and so 302 is returned

    def test_changing_profile_picture(self):
        """
        Parameters:
            self

        Tests whether the user can change their profile picture
        @author: Jonathan Tao, Sam Tebbet, Rhys Broughton
        """
        response = self.client.post(reverse('signup'), HTTP_USER_AGENT="Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_1 like Mac OS X) AppleWebKit/603.1.30 (KHTML, like Gecko) Version/10.0 Mobile/14E304 Safari/602.1", data={
            'username': 'testuser',
            'email': 'testuser@email.com',
            'password1': 'Hjguhjlkjbv765588',
            'password2': 'Hjguhjlkjbv765588'
        })  # create a request to sign-up as a user using the sign-up form

        Avatar.objects.create(
            imageName='https://i.imgur.com/HteIBRi.png',
            avatarTitle='Happy Fish'
        )

        user_account = User.objects.get(username='testuser')
        change_pfp_response = self.client.post(reverse('change_profile_picture'), HTTP_USER_AGENT="Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_1 like Mac OS X) AppleWebKit/603.1.30 (KHTML, like Gecko) Version/10.0 Mobile/14E304 Safari/602.1", data = {
            'chosen_pfp': 'https://i.imgur.com/fhrZmo9.png'
        })

        test_user = UserInfo.objects.get(user=user_account)
        new_avatar = Avatar.objects.get(id=test_user.avatarId_id).imageName
        self.assertEqual(new_avatar, "https://i.imgur.com/fhrZmo9.png")

    def test_change_title(self):
        """
        Parameters:
            self
        Tests whether the user can change their title
        @author: Jonathan Tao, Sam Tebbet
        """
        response = self.client.post(reverse('signup'),HTTP_USER_AGENT="Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_1 like Mac OS X) AppleWebKit/603.1.30 (KHTML, like Gecko) Version/10.0 Mobile/14E304 Safari/602.1", data={
                'username': 'testuser',
                'email': 'testuser@email.com',
                'password1': 'Hjguhjlkjbv765588',
                'password2': 'Hjguhjlkjbv765588'
        })  # create a request to sign-up as a user using the sign-up form

        user_account = User.objects.get(username='testuser')
        test_user = UserInfo.objects.get(user=user_account)
        start_title = test_user.title
        change_title_response = self.client.post(reverse('change_title', kwargs={'title': 'tree'}),HTTP_USER_AGENT="Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_1 like Mac OS X) AppleWebKit/603.1.30 (KHTML, like Gecko) Version/10.0 Mobile/14E304 Safari/602.1", data={})
        changed_test_user = UserInfo.objects.get(user=user_account)
        changed_title = changed_test_user.title
        self.assertNotEqual(start_title, changed_title)
        self.assertEqual(change_title_response.status_code, 302)


class TestAddScore(TransactionTestCase):
    def test_url(self):
        """
        Parameters:
            self

        Tests whether the add score action can be performed by the url itself
        @author: Jonathan Tao
        """

        response = self.client.get('/addScore', HTTP_USER_AGENT = "Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_1 like Mac OS X) AppleWebKit/603.1.30 (KHTML, like Gecko) Version/10.0 Mobile/14E304 Safari/602.1")
        self.assertEqual(response.status_code, 302) #test the status code returned. In this case since this webpage is accessed after login, there is a redirect and so 302 is returned

    def test_url_via_name(self):
        """
        Parameters:
            self

        Tests whether the add score action can be performed by the name associated with the url
        @author: Jonathan Tao
        """

        response = self.client.get(reverse('score'), HTTP_USER_AGENT = "Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_1 like Mac OS X) AppleWebKit/603.1.30 (KHTML, like Gecko) Version/10.0 Mobile/14E304 Safari/602.1")
        self.assertEqual(response.status_code, 302) #test the status code returned. In this case since this webpage is accessed after login, there is a redirect and so 302 is returned

    def test_adding_score(self):
        """
       Parameters:
           self
       Tests whether the users score is updated
       @author: Jonathan Tao, Sam Tebbet
       """

        today = datetime.date.today()
        Spot.objects.create( #create a spot
            name='Duck Pond',
            desc='A duck pond with fountains and nice secluded seating areas. A great place to go and chill between lectures.',
            latitude=50.73439,
            longitude=-3.537932,
            average_attendance=6,
            imageName='https://i.imgur.com/u7yqGqI.jpeg'
        )

        Spot.objects.create( #create another spot for the streak
            name='XFI Common',
            desc="Round the back of the XFI building enjoy this green space with some friends to get the most of a sunny day. If you don't feel like hanging out on the floor there are benches near by.",
            latitude=50.736190,
            longitude=-3.529250,
            average_attendance=0,
            imageName='https://i.imgur.com/zxC3CwO.jpg'
        )
        yesterday_spot = Spot.objects.get(name="XFI Common")
        current_spot = Spot.objects.get(name="Duck Pond")
        yesterday = today - datetime.timedelta(days=1)

        SpotRecord.objects.create( #create a record for the spot
            sId=current_spot,
            attendance=0,
            spotDay=today
        )
        SpotRecord.objects.create( #create another record for the spot
            sId=yesterday_spot,
            attendance=0,
            spotDay=yesterday
        )

        response = self.client.post(reverse('signup'), HTTP_USER_AGENT="Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_1 like Mac OS X) AppleWebKit/603.1.30 (KHTML, like Gecko) Version/10.0 Mobile/14E304 Safari/602.1", data={
            'username': 'testuser',
            'email': 'testuser@email.com',
            'password1': 'Hjguhjlkjbv765588',
            'password2': 'Hjguhjlkjbv765588'
        })  # create a request to sign-up as a user using the sign-up form

        user_account = User.objects.get(username='testuser')
        old_user = UserInfo.objects.get(user=user_account)

        add_score_response = self.client.post(reverse('score'), HTTP_USER_AGENT="Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_1 like Mac OS X) AppleWebKit/603.1.30 (KHTML, like Gecko) Version/10.0 Mobile/14E304 Safari/602.1", data = {
            'star': 3 #give star rating so a score can be added
        })

        user_account = User.objects.get(username='testuser')
        new_user = UserInfo.objects.get(user=user_account)

        now = datetime.datetime.now()
        now_time = now.time()

        # The score should only be added if they add score between 9am and 4pm
        if now_time.hour < 9 or now_time.hour > 16:
            self.assertEqual(old_user.currentStreak, new_user.currentStreak)  # Streak should not increase by 1
            self.assertEqual(old_user.totalPoints, new_user.totalPoints)  # No points should be added
        else:
            self.assertEqual(old_user.currentStreak, new_user.currentStreak - 1)  # Streak should increase by 1
            self.assertEqual(old_user.totalPoints, new_user.totalPoints - 5)  # Technically the first user to reach the spot


class TestPledge(TransactionTestCase):
    def test_url(self):
        """
        Parameters:
            self

        Tests whether the pledge page can be brought up by the url itself
        @author: Jonathan Tao
        """

        response = self.client.get('/pledge', HTTP_USER_AGENT = "Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_1 like Mac OS X) AppleWebKit/603.1.30 (KHTML, like Gecko) Version/10.0 Mobile/14E304 Safari/602.1")
        self.assertEqual(response.status_code, 302) #test the status code returned. In this case since this webpage is accessed after login, there is a redirect and so 302 is returned
    def test_url_via_name(self):
        """
        Parameters:
            self

        Tests whether the pledge page can be brought up by the name associated with the url
        @author: Jonathan Tao
        """

        response = self.client.get(reverse('pledge'), HTTP_USER_AGENT = "Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_1 like Mac OS X) AppleWebKit/603.1.30 (KHTML, like Gecko) Version/10.0 Mobile/14E304 Safari/602.1")
        self.assertEqual(response.status_code, 302) #test the status code returned. In this case since this webpage is accessed after login, there is a redirect and so 302 is returned



class TestTakePledge(TransactionTestCase):
    def test_url(self):
        """
        Parameters:
            self

        Tests whether the take pledge action can be performed by the url itself
        @author: Jonathan Tao
        """

        response = self.client.get('/take_pledge', HTTP_USER_AGENT = "Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_1 like Mac OS X) AppleWebKit/603.1.30 (KHTML, like Gecko) Version/10.0 Mobile/14E304 Safari/602.1")
        self.assertEqual(response.status_code, 302) #test the status code returned. In this case since this webpage is accessed after login, there is a redirect and so 302 is returned

    def test_url_via_name(self):
        """
        Parameters:
            self

        Tests whether the take pledge action can be performed by the name associated with the url
        @author: Jonathan Tao
        """

        response = self.client.get(reverse('takePledge'), HTTP_USER_AGENT = "Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_1 like Mac OS X) AppleWebKit/603.1.30 (KHTML, like Gecko) Version/10.0 Mobile/14E304 Safari/602.1")
        self.assertEqual(response.status_code, 302) #test the status code returned. In this case since this webpage is accessed after login, there is a redirect and so 302 is returned

class TestPrivacyPolicyPage(TransactionTestCase):
    def test_url(self):
        """
        Parameters:
            self

        Tests whether the privacy policy page can be brought up by the url itself
        @author: Jonathan Tao
        """

        response = self.client.get('/privacy_policy', HTTP_USER_AGENT = "Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_1 like Mac OS X) AppleWebKit/603.1.30 (KHTML, like Gecko) Version/10.0 Mobile/14E304 Safari/602.1")
        self.assertEqual(response.status_code, 200) #test the status code returned
        self.assertTemplateUsed(response, template_name='privacy_policy.html')

    def test_url_via_name(self):
        """
        Parameters:
            self

        Tests whether the privacy policy page can be brought up by the name associated with the url
        @author: Jonathan Tao
        """

        response = self.client.get(reverse('privacy_policy'), HTTP_USER_AGENT = "Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_1 like Mac OS X) AppleWebKit/603.1.30 (KHTML, like Gecko) Version/10.0 Mobile/14E304 Safari/602.1")
        self.assertEqual(response.status_code, 200) #test the status code returned
        self.assertTemplateUsed(response, template_name='privacy_policy.html')