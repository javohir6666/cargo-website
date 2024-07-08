from django.db import models
from django.contrib.auth.models import AbstractUser

GENDER_SELECTION = (
    ('Male', 'Male'),
    ('Female', 'Female'),
)


class CustomUser(AbstractUser):
    phone = models.CharField(max_length=17, blank=True, null=True)
    telegram = models.CharField(max_length=150, blank=True, null=True)
    gender = models.CharField(max_length=20, choices=GENDER_SELECTION, blank=True)

    def __str__(self):
        return str(self.username)
    
