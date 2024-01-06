from django.urls import path
from django.contrib import admin
from .views import signup, signin, dashboard, home


urlpatterns = [
    path('admin', admin.site.urls),
    path('', dashboard, name='dashboard'),
    path('login', signin, name='login'),
    path('signup', signup, name='signup'),
    path('home', home, name='home'),
]
