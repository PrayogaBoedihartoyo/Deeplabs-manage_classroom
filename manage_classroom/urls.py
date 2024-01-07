from django.urls import path
from django.contrib import admin
from .views import signup, signin, home, sign_out


urlpatterns = [
    path('admin', admin.site.urls),
    path('', signin, name='login'),
    path('signup', signup, name='signup'),
    path('logout', sign_out, name='logout'),
    path('home', home, name='home'),
]
