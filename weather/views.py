from datetime import datetime, timedelta
import os
import requests
from django.http import JsonResponse
from django.shortcuts import render
from django.contrib.auth.models import User
from .models import SearchHistory

api_key = os.getenv('OPENWEATHER_API_KEY')

def get_weather(request):
    city = request.GET.get('city', '')
    last_searches = []

    default_user, _ = User.objects.get_or_create(username='anonymous_user')

    if city:
        api_url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={api_key}&units=metric"
        
        try:
            response = requests.get(api_url)
            response.raise_for_status()
            weather_data = response.json()

            if weather_data.get('cod') != '200':
                weather_forecast = None
                error = weather_data.get('message', 'Unknown error')
            else:
                weather_forecast = []
                daily_data = {}

                for entry in weather_data['list']:
                    date = datetime.strptime(entry['dt_txt'], '%Y-%m-%d %H:%M:%S')
                    day = date.strftime('%Y-%m-%d')
                    if day not in daily_data:
                        daily_data[day] = {
                            'max_temp': entry['main']['temp_max'],
                            'min_temp': entry['main']['temp_min'],
                            'description': entry['weather'][0]['description'],
                            'icon': entry['weather'][0]['icon'],
                            'hourly': []
                        }
                    else:
                        if entry['main']['temp_max'] > daily_data[day]['max_temp']:
                            daily_data[day]['max_temp'] = entry['main']['temp_max']
                        if entry['main']['temp_min'] < daily_data[day]['min_temp']:
                            daily_data[day]['min_temp'] = entry['main']['temp_min']

                    daily_data[day]['hourly'].append({
                        'time': date.strftime('%H:%M'),
                        'temp': int(entry['main']['temp']),
                        'icon': entry['weather'][0]['icon']
                    })

                for day, data in daily_data.items():
                    weather_forecast.append({
                        'date': day,
                        'max_temp': data['max_temp'],
                        'min_temp': data['min_temp'],
                        'description': data['description'],
                        'icon': data['icon'],
                        'hourly': data['hourly'][:5]
                    })

                SearchHistory.objects.create(
                    user=default_user,
                    city=city,
                    weather_data=weather_data
                )

                error = None

        except requests.exceptions.RequestException as e:
            weather_forecast = None
            error = f"Error fetching weather: {str(e)}"
    else:
        weather_forecast = None
        error = None

    last_searches = SearchHistory.objects.filter(user=default_user).values_list('city', flat=True).distinct()[:3]

    context = {
        'weather_forecast': weather_forecast,
        'error': error,
        'last_searches': list(last_searches),
        'searched_city': city,
    }

    return render(request, 'weather/index.html', context)

def autocomplete(request):
    query = request.GET.get('term', '')
    api_url = f"http://api.openweathermap.org/data/2.5/find?q={query}&type=like&sort=population&cnt=10&appid={api_key}"
    
    try:
        response = requests.get(api_url)
        response.raise_for_status()
        data = response.json()

        suggestions = []
        if 'list' in data:
            for item in data['list']:
                suggestions.append(f"{item['name']}, {item['sys']['country']}")

        return JsonResponse(suggestions, safe=False)
    except requests.exceptions.RequestException as e:
        return JsonResponse([], safe=False)

def search_history(request):
    user_searches = SearchHistory.objects.order_by('-timestamp')
    return render(request, 'weather/search_history.html', {'user_searches': user_searches})