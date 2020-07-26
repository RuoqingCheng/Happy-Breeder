from django.conf.urls import url
from django.urls import path
from .views import *


app_name = ''  # here for namespacing of urls.

urlpatterns = [
    url(r"^$", welcome, name="welcome"),
    url(r"template", template, name="template"),
    url(r"signup", signup.as_view(), name='signup'),
    path("home/", breederhome, name='breederhome'),
    path("useless/", visitothers, name='go_visit'),
    path("other/", seeothers, name='seeothers'),
    path("blush_visit/", daodan, name='daodan'),
    path("buy_item/", buy_item, name="buy_item"),
    path("action/", action, name="action"),
    path("change_pos/", change_pos, name="change_pos"),
    path("auto_update/", auto_update, name="auto_update"),
]
