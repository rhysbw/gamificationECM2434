from django.test import TestCase
from django.urls import reverse

# Create your tests here.
class SignUpTests(TestCase):

    def test_url(self):
        """
        Parameters:
            self

        Tests whether the signing up webpage can be brought up by the url itself
        """
        response = self.client.get('/signup', HTTP_USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36")
        self.assertEqual(response.status_code, 200) #test the status code returned
        self.assertTemplateUsed(response, template_name='QRCodePage.html') #test the template used

    def test_url_via_name(self):
        """
        Parameters:
            self

        Tests whether the signing up webpage can be brought up by the name associated with the url
        """
        response = self.client.get(reverse('signup'), HTTP_USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36")
        self.assertEqual(response.status_code, 200) #test the status code returned
        self.assertTemplateUsed(response, template_name='QRCodePage.html') #test the template used

class LoginTests(TestCase):

    def test_url(self):
        """
        Parameters:
            self

        Tests whether the login webpage can be brought up by the url itself
        """
        response = self.client.get('/login/', HTTP_USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36")
        self.assertEqual(response.status_code, 200) #test the status code returned
        self.assertTemplateUsed(response, template_name='QRCodePage.html') #test the template used

    def test_url_via_name(self):
        """
        Parameters:
            self

        Tests whether the login webpage can be brought up by the name associated with the url
        """
        response = self.client.get(reverse('login'), HTTP_USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36")
        self.assertEqual(response.status_code, 200) #test the status code returned
        self.assertTemplateUsed(response, template_name='QRCodePage.html') #test the template used


