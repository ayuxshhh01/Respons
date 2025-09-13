from django.contrib.auth.models import AbstractUser,AbstractBaseUser
from django.db import models

class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length=15, blank=True)
    emergency_contact = models.CharField(max_length=15, blank=True)
    safety_score = models.IntegerField(default=90)
    blockchain_id = models.CharField(max_length=100, blank=True)
    last_location_update = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.username

class Alert(models.Model):
   
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    
    
    alert_type = models.CharField(max_length=50) 
    
    location = models.JSONField() 
    
    timestamp = models.DateTimeField(auto_now_add=True)

    heart_rate = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.alert_type} for {self.user.username} at {self.timestamp}"
    



class GeoZone(models.Model):
    name = models.CharField(max_length=100)
    # For "dangerous/restricted areas".
    zone_type = models.CharField(max_length=50, default='High-Risk') 
    center_lat = models.FloatField()
    center_lon = models.FloatField()
    radius_km = models.FloatField()

    def __str__(self):
        return self.name
    


class Itinerary(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    # Stores the output of the "Smart itinerary planner".
    plan_data = models.JSONField()