
import os
from pprint import pprint

from django.contrib import messages
from django.contrib.auth import authenticate, get_user_model, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import UpdateView, ListView, DetailView, FormView
from orders.models import OrderItem, Order, User
from django.shortcuts import render, get_object_or_404, redirect

from .forms import SignUpForm, LoginForm, UserPgpChangeForm, GPGAuthForm
from dark_web.mixins import RequestFormAttachMixin
from accounts.models import VendorTerm,User as VendorUser
from star_ratings.models import Rating,UserRating
from main.models import Product
from main.views import cryptocurrencies


# Create your views here.


# User ORDER details page
class UserOrderDetailView(LoginRequiredMixin, DetailView):
    template_name = 'orders/order-detail.html'

    def get_object(self, queryset=None):
        order_id = self.kwargs.get("order_id")
        orders = OrderItem.objects.filter(order_id=order_id, author=self.request.user)
        return orders.first()


# User ORDER(s) page
class UserOrdersListView(LoginRequiredMixin, ListView):
    template_name = 'orders/order-list.html'

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)


# User PROFILE update page
class UserPgpUpdateView(LoginRequiredMixin, FormView):
    form_class = UserPgpChangeForm
    template_name = "profile/update-pgp.html"

    def get_context_data(self, **kwargs):
        context = super(UserPgpUpdateView, self).get_context_data(**kwargs)
        context['pgp_form'] = UserPgpChangeForm
        return context

    # def get_object(self, queryset=None):
    #     return self.request.user

    def form_valid(self, form):
        print("Valid")
        request = self.request
        user = self.request.user
        print(request.user)
        print(form.cleaned_data)
        pgp_key = form.cleaned_data.get('pgp_key')
        user.pgp_key = pgp_key
        user.save()
        print("Confirm")
        print(user.pgp_key)
        msg = "PGP Key updated successfully"
        messages.success(request, msg)
        return redirect("user_profile")

    def form_invalid(self, form):
        print("Invalid")
        request = self.request
        msg = "Form invalid"
        messages.success(request, msg)
        return redirect("user_profile")


# User PROFILE page
class UserProfileView(LoginRequiredMixin, DetailView):
    template_name = "profile/user-profile.html"

    # def get_context_data(self, **kwargs):
    #     context = super(UserProfileView, self).get_context_data(**kwargs)
    #     context['pgp_form'] = UserPgpChangeForm
    #     return context

    def get_object(self, queryset=None):
        return self.request.user


# User Sign-up View
def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            raw_password = form.cleaned_data.get('password1')
            user_ = form.save()
            user = authenticate(username=user_.username, password=raw_password)
            login(request, user)

            msg = "Hello " + user.username.upper() + ". Welcome to OnionShop."
            messages.success(request, msg)
            return redirect("product_list")
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})


#GPG auth
def gpgauth(request):
    #decrypt randomstring with users
    user = User.objects.get(username = request.session['username'])
    gpg = gnupg.GPG()
    import_result = gpg.import_keys(user.pgp_key)
    pprint(import_result.results)

    encrypted_data = gpg.encrypt(request.session['orgkey'], import_result.fingerprints[0], armor=True, always_trust=True)
    encrypted_string = str(encrypted_data)
    print (str(encrypted_data.ok))
    print(encrypted_string)
    return render(request, "gpgauth.html", {"encmessage" : encrypted_string})


def gpgverify(request):

    error_url = '/signin/gpgauth/'
    success_url = '/'

    if request.method == 'POST':

        message = request.POST['message']

        if message != request.session['orgkey']:
            msg = "Invalid Key"
            messages.error(request, msg)
            return redirect(error_url)

        username = request.session['username']
        password = request.session['password']
        user = authenticate(request, username=username, password=password)
        login(request, user)
        msg = "Welcome back " + user.username.upper()
        messages.success(request, msg)
        return redirect(success_url)

    msg = "Error Invalid Key"
    messages.error(request, msg)
    return redirect(error_url)


# User Sign-in View
class LoginView(RequestFormAttachMixin, FormView):
    form_class = LoginForm
    success_url = '/signin/gpgauth/'
    template_name = "registration/login.html"

    def form_valid(self, form):
        request = self.request
        user = request.user
        users = User.objects.get(username = request.session['username'])
        if str(users.pgp_key) == "None":
            user = authenticate(request, username=request.session['username'], password=request.session['password'])
            login(request, user)
            msg = "Welcome back " + user.username.upper()
            messages.success(request, msg)
            self.success_url = "/"
        if users.tfalogin == False:
            msg = "Welcome back " + user.username.upper()
            messages.success(request, msg)
            self.success_url = "/"
        return redirect(self.success_url)

#Use 2fa pgp login
def usetfalogin(request):
    user = User.objects.get(username = request.session['username'])
    user.tfalogin = request.POST['loginmethod']
    user.save()
    messages.success(request, "Successed")
    return redirect("user_profile")

#vendor Public Profile View
def vendorProfile(request,id=None):
    if request.method == 'GET' and id is not None or id is not "":
        vendor=User.objects.values('pgp_key').filter(id=id)
    else:
        raise Exception("404")

    context={
        'user':vendor[0]
    }
    return render(request,'profile/vendor-profile.html',context)

def vendorPublicProfile(request,id=None):
    vendorProducts=Product.objects.filter(productOwnerID=id)
    ratingdict={}
    for vendorProduct in vendorProducts:
        ratings = Rating.objects.filter(object_id=vendorProduct.id)
        if ratings:
            ratingsObject = UserRating.objects.filter(rating=ratings[0].id)
            ratingsObject = ratingsObject[0]
            ratingdict.update([(ratingsObject,vendorProduct.name)])

        else:
            ratingsObject = None
    vendorUser=VendorUser.objects.filter(id=id)
    vendorTerm=VendorTerm.objects.filter(userId=id)
    cryptoData = cryptocurrencies()
    context={
        "vendorUser":vendorUser[0],
        "vendorTerm":vendorTerm[0].description,
        "ratingsDict":ratingdict,
        "cryptoData":cryptoData
    }
    return render(request, 'profile/vendor-public-profile.html',context)


