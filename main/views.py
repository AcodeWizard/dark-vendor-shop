from cart.forms import CartAddProductForm
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
# from django.core.urlresolvers import reverse
from django.views.generic import UpdateView
from orders.models import OrderItem, Order
from django.shortcuts import render, get_object_or_404, redirect
from cryptowatch_client import Client

from .models import Category, Product
from django_countries import countries
from accounts.models import User
from django.db.models import Q
from star_ratings.models import Rating,UserRating

# def signup(request):
#     if request.method == 'POST':
#         form = SignUpForm(request.POST)
#         if form.is_valid():
#             user = form.save()
#             msg = "Hello " + user.username + ". Welcome to OnionShop."
#             messages.success(request, msg)
#             return redirect("product_list")
#     else:
#         form = SignUpForm()
#     return render(request, 'registration/signup.html', {'form': form})
#
#
# def signin(request):
#     if request.method == 'POST':
#         form = LoginForm(request.POST)
#         if form.is_valid():
#             user = form.save()
#             msg = "Welcome back" + user.username
#             messages.success(request, msg)
#             return redirect("product_list")
#     else:
#         form = LoginForm(request)
#     return render(request, 'registration/login.html', {'form': form})
def cryptocurrencies():
    client = Client(timeout=30)
    btcgbp = client.get_markets_price(exchange='gdax', pair='btcgbp')
    btcusd = client.get_markets_price(exchange='gdax', pair='btcusd')
    btceur = client.get_markets_price(exchange='gdax', pair='btceur')
    btcgbp_response = btcgbp.json()
    btcusd_response = btcusd.json()
    btceur_response = btceur.json()
    btcgbpPrice=btcgbp_response.get('result').get('price')
    btcusdPrice=btcusd_response.get('result').get('price')
    btceurPrice=btceur_response.get('result').get('price')
    cryptoPrice={"btcusd":btcusdPrice,'btcgbp':btcgbpPrice,'btceur':btceurPrice}
    return cryptoPrice

def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(category=category)

    #cryptocurrenies Data
    cryptoData=cryptocurrencies()

    context = {
        'category': category,
        'categories': categories,
        'products': products,
         'cryptoData':cryptoData,
        'countries':countries

    }


    return render(request, 'main/product/list.html', context)


def product_detail(request, id, slug):
    product = get_object_or_404(Product, id=id, slug=slug, available=True)
    cart_product_form = CartAddProductForm()
    productVendor=Product.objects.values('productOwnerID','country').get(id=id)
    country=productVendor.get('country')
    productVendor=productVendor.get('productOwnerID')

    vendor=User.objects.values('id','username').filter(id=productVendor,vendor=True)
    ratings=Rating.objects.filter(object_id=id)
    if ratings:
        ratingsObject=UserRating.objects.filter(rating=ratings[0].id)
        ratingsObject=ratingsObject[0]
    else:
        ratingsObject=None
    context = {
        'product': product,
        'cart_product_form': cart_product_form,
        'vendor':vendor[0],
        'country':country,
        'ratingsObject':ratingsObject
    }
    return render(request, 'main/product/detail.html', context)
def search(request):
    if request.method == 'GET':
        price=None
        if request.GET.get('price'):
            price = int(request.GET.get('price'))
        country=request.GET.get('country', None)
        category=request.GET.get('category', None)
        categoryID=Category.objects.filter(name=category)
        products={}
        if price and category=="" and country=="":
            products=Product.objects.filter(Q(price__gte=price) | Q(price=price))
        elif category and price==None and country=="":
            products=Product.objects.filter(category__in=categoryID)
        elif country and price==None and category=="":
            products=Product.objects.filter(country=country)
        elif price and category and country=="":
            products=Product.objects.filter(Q(price__gte=price)|Q(price=price),category__in=categoryID)
        elif country and price and category=="":
            products=Product.objects.filter(Q(price__gte=price)|Q(price=price),country=country)
        elif country and category and price==None:
            products=Product.objects.filter(country=country ,category__in=categoryID)
        elif price and category and country:
            products=Product.objects.filter(Q(price__gte=price)|Q(price=price),category__in=categoryID ,country=country)

        categories = Category.objects.all()
        # cryptocurrenies Data
        cryptoData = cryptocurrencies()

        context = {
            'category': category,
            'categories': categories,
            'products': products,
            'cryptoData': cryptoData,
            'countries': countries

        }


    else:
        raise  Exception("405")
    return render(request, 'main/product/list.html', context)

# def user_profile(request):
#     if request.user.is_authenticated:
#         context = {
#             'object': request.user,
#         }
#         return render(request, 'main/profile/user-profile.html', context)
#     else:
#         return render(request, 'main/nlogin.html')
#
#
# class UserProfileUpdateView(LoginRequiredMixin, UpdateView):
#     form_class = UserProfileChangeForm
#
#     def get_object(self, queryset=None):
#         return self.request.user
#
#     def get_success_url(self):
#         return redirect("user_profile")
#
#
# def profile_orders(request):
#     if request.user.is_authenticated is True:
#         orders = Order.objects.filter(user=request.user)
#         context = {
#             'orders': orders,
#         }
#         return render(request, 'main/profile/order-list.html', context)
#     else:
#         return render(request, 'main/nlogin.html')
#
#
# def profile_order(request, order_id):
#     if request.user.is_authenticated is True:
#         orders = OrderItem.objects.filter(order_id=order_id, author=request.user)
#
#         context = {
#             'orders': orders,
#         }
#         return render(request, 'main/profile/order-detail.html', context)
#     else:
#         return render(request, 'main/nlogin.html')
#
