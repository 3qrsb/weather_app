from django.urls import path
from .views import get_weather, autocomplete, search_history, search_count

urlpatterns = [
    path('', get_weather, name='get_weather'),
    path('autocomplete/', autocomplete, name='autocomplete'),
    path('history/', search_history, name='search_history'),
    path('search-count/', search_count, name='search_count'),
]