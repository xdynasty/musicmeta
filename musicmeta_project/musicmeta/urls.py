from django.urls import path
from . import views


app_name = 'musicmeta'
urlpatterns = [
    path('', views.index, name="index"),
]
