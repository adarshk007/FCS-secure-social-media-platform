"""FCS URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth import views as auth_views

from account.views import (
	registration_view, 
	login_view, 
	logout_view
)

from dashboard.views import (
	dashboard_view,

    profile_view,
    edit_profile_info_view,
    change_password_view,

    send_request_view,
    accept_request_view,
    delete_request_view,
    unfriend_view,
    friends_view,
    friend_requests_view,

    search_view,

    wallet_view,
    add_money_view,
    transfer_money_view,
    transactions_view,
    accept_transaction_view,
    decline_transaction_view,
    accept_decline_transaction_view,

    messenger_view,
    messenge_view,
    create_group_view,

    create_post_view,

    upgrade_view,
    upgrade_payment_view,

    create_page_view,
    page_view,
)

from home.views import (
	home_view
)

urlpatterns = [
    url(r'^adminterigg/', admin.site.urls),

    url(r'^dashboard/$', dashboard_view, name = "dashboard"),
    
    url(r'^login/$', login_view, name="login"),
    url(r'^register/$', registration_view, name="register"),
    url(r'^logout/$', logout_view, name="logout"),


    url(r'^profile/password/$', change_password_view, name="change_password"),
    url(r'^profile/edit/$', edit_profile_info_view, name="edit_profile_info"),
    url(r'^profile/(?P<u_id>\w+)/$', profile_view, name="profile"),
    url(r'^profile/(?P<u_id>\w+)/send_request/$', send_request_view, name="send_request"),
    url(r'^profile/(?P<u_id>\w+)/unfriend/$', unfriend_view, name="unfriend"),
    url(r'^profile/(?P<u_id>\w+)/accept_request/$', accept_request_view, name="accept_request"),
    url(r'^profile/(?P<u_id>\w+)/delete_request/$', delete_request_view, name="delete_request"),



    url(r'^friends/$', friends_view, name="friends"),
    url(r'^friend_requests/$', friend_requests_view, name="friend_requests"),
    
    url(r'^search/$', search_view, name="search"),


    url(r'^messenger/create_group/$', create_group_view, name="create_group"),
    url(r'^messenger/$', messenger_view, name="messenger"),
    url(r'^messenger/(?P<user_1>\w+)/(?P<user_2>\w+)/$', messenge_view, name="my_message"),



    url(r'^wallet/add_money/$', add_money_view, name="add_money"),
    url(r'^wallet/transfer_money/$', transfer_money_view, name="transfer_money"),
    url(r'^wallet/transactions/$', transactions_view, name="transactions"),
    url(r'^wallet/$', wallet_view, name="wallet"),
    url(r'^accept_transaction/(?P<t_id>\w+)/$', accept_transaction_view, name="accept_transaction"),
    url(r'^decline_transaction/(?P<t_id>\w+)/$', decline_transaction_view, name="decline_transaction"),
    url(r'^accept_decline_transaction/$', accept_decline_transaction_view, name="accept_decline"),
        
    url(r'^create_post/(?P<u_id>\w+)/$', create_post_view, name="create_post"),
    url(r'^upgrade/$', upgrade_view, name="upgrade"),
    url(r'^upgrade/(?P<type>\w+)/$', upgrade_payment_view, name="upgrade"),
  
    url(r'^create_page/$', create_page_view, name="create_page"),
    url(r'^page/(?P<id>\w+)/$', page_view, name="page"),
    
        

    url(r'^$', home_view, name="home"),
]
