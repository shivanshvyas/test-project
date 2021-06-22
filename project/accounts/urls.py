from accounts import views
from django.conf.urls import url
from django.contrib import admin
from django.urls import reverse_lazy

from .views import *

admin.autodiscover()

app_name = 'accounts'

urlpatterns = [
    url(r'^login/$', login_user, name='login'),
    url(r'^signup/$', register, name='signup'),
    url(r'^profile/$', profile, name='profile'),
    url(r'^home_page/$', home_page, name='home_page'),
    ]