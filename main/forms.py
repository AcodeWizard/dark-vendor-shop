from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import ReadOnlyPasswordHashField

from captcha.fields import CaptchaField


# class SignUpForm(UserCreationForm):
#     captcha = CaptchaField()
#
#     class Meta:
#         model = User
#         fields = ('username', 'password1', 'password2', )
#
#     def clean_password2(self):
#         # Check that the two password entries match
#         password1 = self.cleaned_data.get("password1")
#         password2 = self.cleaned_data.get("password2")
#         if password1 and password2 and password1 != password2:
#             raise forms.ValidationError("Passwords don't match")
#         return password2
#
#     def clean(self):
#         request = self.request
#         cleaned_data = self.cleaned_data
#         username = cleaned_data.get('username')
#         raw_password = cleaned_data.get('password1')
#         user = authenticate(username=username, password=raw_password)
#         login(request, user)
#         return cleaned_data
#
#
# class LoginForm(forms.Form):
#     username = forms.CharField(widget=forms.TextInput)
#     password = forms.CharField(widget=forms.PasswordInput)
#
#     captcha = CaptchaField()
#
#     def __init__(self, request, *args, **kwargs):
#         self.request = request
#         super(LoginForm, self).__init__(*args, **kwargs)
#
#     def clean(self):
#         request = self.request
#         data = self.cleaned_data
#         username = data.get("username")
#         password = data.get("password")
#
#         user = authenticate(request, username=username, password=password)
#         if user is None:
#             raise forms.ValidationError("Invalid username or password")
#         login(request, user)
#
#         return data
#
#
# class UserProfileChangeForm(forms.Form):
#     password = ReadOnlyPasswordHashField()
#
#     class Meta:
#         model = User
#         fields = ['username', 'password', 'password']
#
#     def clean_password(self):
#         # Regardless of what the user provides, return the initial value.
#         # This is done here, rather than on the field, because the
#         # field does not have access to the initial value
#         return self.initial["password"]