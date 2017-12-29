from django.conf.urls import url
from . import views
from models import *

urlpatterns = [
    url(r'^$', views.index),
    url(r'^users/(?P<user_id>\d+)$', views.show_user),
    url(r'^logout$', views.logout),
    url(r'^books/(?P<book_id>\d+)$', views.show_book),
    url(r'^books$', views.welcome),
    url(r'^books/add$', views.add_review),
    url(r'^logout$', views.logout),
    url(r'^addbookshort/(?P<book_id>\d+)$', views.addbookshort),
    url(r'^(?P<action>\w+)$', views.process),
]