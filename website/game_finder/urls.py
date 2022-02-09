from django.urls import path
from . import views

app_name = 'game_finder'

urlpatterns = [
    path('', views.home, name='home'),
    path('search/', views.search, name='search-results'),
    path('who-made-me/', views.whomade, name='whomade'),
    path('about/', views.about, name='about'),
]


