from django.urls import path, include
from django.conf.urls import url

from . import views as account_views

urlpatterns = [
    path('', include("accounts.passwords.urls")),
    path('accounts/', include('django.contrib.auth.urls')),

    # url(r'^profile/update/pgp-key/$', account_views.UserPgpUpdateView.as_view(), name='user_pgp_update'),


    url(r'^profile/update/pgp-key/$', account_views.UserPgpUpdateView.as_view(), name='user_pgp_update'),
    url(r'^profile/', account_views.UserProfileView.as_view(), name='user_profile'),


    # User Order(s)
    url(r'^orders/$', account_views.UserOrdersListView.as_view(), name='user_order_list'),
    url(r'^orders/(?P<order_id>\d+)/$', account_views.UserOrderDetailView.as_view(), name='user_order_detail'),

]
