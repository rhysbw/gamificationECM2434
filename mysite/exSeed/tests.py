from django.test import TestCase
from django.urls import reverse

# Create your tests here.
class SignUpTests(TestCase):
    def set_user(self):
        self.username = 'JTao'
        self.email = 'jtao@gmail.com'
        self.password = 'HelloWorld'

    def test_url(self):
        response = self.client.get('/signup', HTTP_USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='QRCodePage.html')

    def test_url_via_name(self):
        response = self.client.get(reverse('signup'), HTTP_USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='QRCodePage.html')

class LoginTests(TestCase):

    def set_user(self):
        self.username = 'JTao'
        self.password = 'HelloWorld'

    def test_url(self):
        response = self.client.get('/login/', HTTP_USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='QRCodePage.html')

    def test_url_via_name(self):
        response = self.client.get(reverse('login'), HTTP_USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='QRCodePage.html')


