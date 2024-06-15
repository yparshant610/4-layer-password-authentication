# models.py
from django.contrib.auth.models import User
from django.db import models

class UserDevice(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    device_name = models.CharField(max_length=100)
    last_login = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s {self.device_name}"
