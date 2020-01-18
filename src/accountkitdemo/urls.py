from django.urls import path
from django.contrib import admin

from logindemo.views import render_login_page

urlpatterns = [

    path('admin/', admin.site.urls),
    path('login', render_login_page, name='login-page'),
]
