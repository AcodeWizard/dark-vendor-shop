from io import BytesIO
from django import forms
from django.contrib import messages
from django.core.files.base import ContentFile
from django.utils.safestring import mark_safe
from PIL import Image

from django import forms
from django.contrib.auth import authenticate, get_user_model, login
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth.password_validation import validate_password

from captcha.fields import CaptchaField

import string
import random

User = get_user_model()

def randomstring(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

class UserPgpChangeForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['pgp_key']


class LoginForm(forms.Form):
    """A form to sign-in authenticated users. Includes a simple captcha challenge."""
    username = forms.CharField(widget=forms.TextInput)
    password = forms.CharField(widget=forms.PasswordInput)

    captcha = CaptchaField()

    def __init__(self, request, *args, **kwargs):
        self.request = request
        super(LoginForm, self).__init__(*args, **kwargs)

    def clean_password(self):
        request = self.request
        cleaned_data = self.cleaned_data
        username = cleaned_data.get("username")
        password = cleaned_data.get("password")

        user = authenticate(request, username=username, password=password)
        if user is None:
            raise forms.ValidationError("Invalid username or password")
        if user.tfalogin == False:
            login(request, user)
        request.session['username'] = user.username
        request.session['password'] = password
        request.session['orgkey'] = randomstring()
        return password

class GPGAuthForm(forms.Form):

    def __init__(self, request, *args, **kwargs):
        self.request = request
        super(GPGAuthForm, self).__init__(*args, **kwargs)


class SignUpForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
        fields, plus a repeated password."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    captcha = CaptchaField()

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', )

    def clean_password1(self):
        # Validate password using built-in Django validator.
        password1 = self.cleaned_data.get("password1")
        validity_errors = validate_password(password1)  # , user=None, password_validators=None)
        if not validity_errors:
            return password1

    def clean_password2(self):
        # Check that the two password entries match
        print("Cleaning password 2")
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the User and pas instance to the form
        print("1_")
        user = super(SignUpForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        print("2_")
        if commit:
            user.save()
        return user


# Form for updating users in the ADMIN site
class UserAdminChangeForm(forms.ModelForm):
    """A form for updating users on the ADMIN site.
    Includes all the fields on the user, but replaces the
    password field with admin's password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ('username', )  # 'pgp_key', 'image', 'password', 'admin', 'staff', 'vendor', 'is_active')

    def clean_password(self):
        # Regardless of what input is provided, returns the initial password value.
        # This is done so that only authenticated user can change password.
        # Password Change form is handled using Django's built in form.
        return self.initial["password"]


# Form for creating users in the ADMIN site
class UserAdminCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', )

    def clean_password1(self):
        # Validate password using built-in Django validator.
        password1 = self.cleaned_data.get("password1")
        validity_errors = validate_password(password1)  # , user=None, password_validators=None)
        print(validity_errors)
        if not validity_errors:
            return password1

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserAdminCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user
