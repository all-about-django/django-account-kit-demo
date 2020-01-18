from django.urls import path
from django.contrib import admin

from logindemo.views import (
    render_login_page,
    process_login,
)

urlpatterns = [

    path('', render_login_page, name='login-page'),
    path('admin/', admin.site.urls),
    path('sendcode', process_login, name='login-process'),
]
