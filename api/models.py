from django.contrib.auth.models import AbstractUser,AbstractBaseUser
from django.db import models

class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length=15, blank=True)
    emergency_contact = models.CharField(max_length=15, blank=True)
    safety_score = models.IntegerField(default=90)
    blockchain_id = models.CharField(max_length=100, blank=True)

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