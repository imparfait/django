from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('artist/<int:artist_id>/', views.artist_detail, name='artist_detail'),
    path('artist/<int:artist_id>/gallery/', views.artist_gallery, name='artist_gallery'),
]