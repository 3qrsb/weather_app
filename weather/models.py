from django.db import models
from django.contrib.auth.models import User

class SearchHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    city = models.CharField(max_length=100)
    timestamp = models.DateTimeField(auto_now_add=True)
    weather_data = models.JSONField()

    class Meta:
        ordering = ['-timestamp']
