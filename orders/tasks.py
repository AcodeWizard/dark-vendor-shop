
from __future__ import absolute_import, unicode_literals
from .celery import app
from .models import Pay,Order
from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException
from django.utils import timezone

@app.task
def add(x, y):
    return x + y

@app.task
def update(order_id,addres,cost):
   rpc_user = "NSA12012"
   rpc_password = "ZIwnhqsa"
   rpc_connection = AuthServiceProxy("http://%s:%s@213.227.140.1:8332" % (rpc_user, rpc_password))
   transaction = Pay.objects.filter(address=addres)
   rec = rpc_connection.getreceivedbyaddress(addres)
   if float(rec) == float(cost):
       transaction.update(status=2, amount_received=rec)
       order = Order.objects.filter(id=order_id)
       order.update(paid=True)
       return "thanks you have paid"
   else:
       transaction.update(status=1, amount_received=rec)
