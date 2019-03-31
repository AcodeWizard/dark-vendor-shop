
from django.conf.urls import url
from . import views

app_name = 'orders'

urlpatterns = [
    url(r'^create/$', views.order_create, name='order_create'),
    url(r'^(?P<order_id>\d+)/pay/$', views.pay, name='pay'),
    url(r'^waiting/(?P<order_id>\d+)/(?P<addres>[-\w]+)/(?P<cost>\d+\.\d{8})$', views.waiting, name='waiting'),
]
