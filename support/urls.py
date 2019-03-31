from django.conf.urls import url, include
from . import views

app_name = 'support'

urlpatterns =[

    url('^$', views.support_list, name='support_list'),
    url('^customer_chat/$', views.customer_support, name='customer_support'),
    url('^customer_ticket_list/$', views.customer_ticket_list, name='customer_ticket_list'),
    url(r'^customer_ticket/(?P<c_id>\d+)', views.customer_ticket, name='customer_ticket'),
    url('^create_ticket/$', views.create_ticket, name='create_ticket'),
    url('^customer_post_message/$', views.customer_post_message, name='customer_post_message'),
    url('^customer_post_ticket/$', views.customer_post_ticket, name='customer_post_ticket'),
    url('^customer_ticket_replay/$', views.customer_ticket_replay, name='customer_ticket_replay'),
    url(r'^ticket_state_change/(?P<state>\d+)/(?P<ticket_id>\d+)', views.ticket_state_change, name='ticket_state_change'),

    url('^admin_support/$', views.admin_support, name='admin_support'),
    url('^(?P<user>[-\w]+)/$', views.admin_support_user, name='admin_support_user'),
    url('^(?P<user>[-\w]+)/admin_post_message/$', views.admin_post_message, name='admin_post_message'),

]
