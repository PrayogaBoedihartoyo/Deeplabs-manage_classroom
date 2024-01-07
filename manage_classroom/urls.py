from django.urls import path
from django.contrib import admin
from .views import signup, signin, home


urlpatterns = [
    path('admin', admin.site.urls),
    path('', signin, name='login'),
    path('signup', signup, name='signup'),
    path('home', home, name='home'),
]
