from django.urls import path
from .views import get_weather, autocomplete, search_history

urlpatterns = [
    path('', get_weather, name='get_weather'),
    path('autocomplete/', autocomplete, name='autocomplete'),
    path('history/', search_history, name='search_history'),
]