from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.dmdb_messages, name='dmdb_messages'),
]