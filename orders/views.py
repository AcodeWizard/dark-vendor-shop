from django.shortcuts import render,redirect
from .models import OrderItem,Order,Pay
from .forms import OrderCreateForm
from cart.cart import Cart
from accounts.forms import SignUpForm
from django.contrib.auth import login, authenticate
import requests
from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException
from django.utils import timezone
from .tasks import update
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse

"""
rememeber to add cart.clear()
"""


def waiting(request,order_id, addres, cost):
   update.apply_async((order_id,addres,cost),countdown=1200)
   return render(request,"orders/order/waiting.html",{})


def pay(request, order_id):
    cart = Cart(request)
    btc_course = (requests.get("https://api.coindesk.com/v1/bpi/currentprice/USD.json").json())["bpi"]['USD']["rate_float"]
    total_price = cart.get_total_price()
    btc_price = round((float(cart.get_total_price())/float(btc_course)),8)
    rpc_user = "NSA12012"
    rpc_password = "ZIwnhqsa"
    rpc_connection = AuthServiceProxy("http://%s:%s@213.227.140.1:8332"%(rpc_user, rpc_password))
    addres = rpc_connection.getnewaddress()
    pay = Pay.objects.create(timestamp=timezone.now(), amount_expected = btc_price, amount_received = 0, author = request.user.username, status = 0, address = addres)
    pay.save()
    Order.objects.filter(id=order_id).update(payment=pay)
    cart.clear()
    return render(request, 'orders/order/pay.html', {'order_id':order_id,'addres':addres,'btc_course': btc_course, "total_price":total_price, "btc_price":btc_price})


def order_create(request):
    cart = Cart(request)
    if request.user.is_authenticated == True:
        if request.method == 'POST':
            form = OrderCreateForm(request.POST)
            if form.is_valid():
                order = Order.objects.create(
                    user = request.user,
                    address = form['address'].value())
                for item in cart:
                    OrderItem.objects.create(
                        author=request.user,
                        order=order,
                        product=item['product'],
                        price=item['price'],
                        quantity=item['quantity']
                    )
            return HttpResponseRedirect(reverse('orders:pay', args=[order.id]))
        else:
            form = OrderCreateForm()
        return render(request, 'orders/order/create.html', {'form': form})
    elif request.user.is_authenticated == False:
        if request.method == 'POST':
            form = SignUpForm(request.POST)
            if form.is_valid():
                form.save()
                username = form.cleaned_data.get('username')
                raw_password = form.cleaned_data.get('password1')
                user = authenticate(username=username, password=raw_password)
                login(request, user)
                return redirect('orders:order_create')
            else:
                form = SignUpForm()
                return render(request, 'orders/order/create.html', {'form': form})
        else:
            form = SignUpForm()
            return render(request, 'orders/order/create.html', {'form': form})
        return redirect('orders:order_create')




