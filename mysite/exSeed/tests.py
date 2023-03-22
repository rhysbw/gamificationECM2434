from django.test import TransactionTestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

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