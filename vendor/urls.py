from django.urls import path, include
from django.conf.urls import url

from . import views as vendor_views


urlpatterns = [
    url(r'^/$', vendor_views.UserVendorView.as_view(), name='user_vendor'),
    url(r'^/additem$', vendor_views.UserAddItemView.as_view(), name='user_vendor_add_item'),


]
