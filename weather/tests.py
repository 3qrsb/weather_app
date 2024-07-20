from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User

class WeatherAppTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create(username='test_user')

    def test_get_weather_view(self):
        response = self.client.get(reverse('get_weather'), {'city': 'Astana'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'weather/index.html')

    def test_autocomplete_view(self):
        response = self.client.get(reverse('autocomplete'), {'term': 'Ast'})
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json(), list)
        
    def test_search_count_view(self):
        response = self.client.get(reverse('search_count'))
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json(), list)
        
    def test_search_count_increment(self):
        initial_response = self.client.get(reverse('get_weather'), {'city': 'Astana'})
        self.assertEqual(initial_response.status_code, 200)

        initial_count_response = self.client.get(reverse('search_count'))
        initial_counts = initial_count_response.json()
        initial_count = next((item['count'] for item in initial_counts if item['city'] == 'Astana'), 0)

        self.client.get(reverse('get_weather'), {'city': 'Astana'})

        incremented_count_response = self.client.get(reverse('search_count'))
        incremented_counts = incremented_count_response.json()
        incremented_count = next((item['count'] for item in incremented_counts if item['city'] == 'Astana'), 0)

        self.assertEqual(incremented_count, initial_count + 1)
