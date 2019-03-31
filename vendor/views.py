
import os
from pprint import pprint

from django.contrib import messages
from django.contrib.auth import authenticate, get_user_model, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import UpdateView, ListView, DetailView, FormView
from orders.models import OrderItem, Order, User
from django.shortcuts import render, get_object_or_404, redirect


from dark_web.mixins import RequestFormAttachMixin


# User vendor page
class UserVendorView(LoginRequiredMixin, DetailView):
    template_name = "mysales.html"

    def get_object(self, queryset=None):
        return self.request.user

# User add item page
class UserAddItemView(LoginRequiredMixin, DetailView):
    template_name = "newitem.html"

    def get_object(self, queryset=None):
        return self.request.user
