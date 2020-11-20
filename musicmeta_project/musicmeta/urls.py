from django.urls import path
from . import views


app_name = 'musicmeta'
urlpatterns = [
    path('', views.index, name="index"),
    path('artist/<str:artist_id>/<int:page>/', views.artist, name="artist")
]
