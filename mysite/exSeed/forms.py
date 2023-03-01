from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class SignupForm(UserCreationForm):
    """
    Class SignupForm
    Declares the fields in the form for registration: referenced in views.signup

    @author: Sam Tebbet
    """
    email = forms.EmailField(max_length=200, help_text='Required')  # adds email functionality

    class Meta:
        """
        class Meta
        For the signup form, declared the fields.

        @author Sam Tebbet
        """
        model = User
        fields = ('username', 'email', 'password1', 'password2')  # The fields in the form
