from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    travel_plans = models.ManyToManyField('TravelPlan', related_name="passengers")

class TravelPlan(models.Model):
    name = models.CharField(max_length=255)
    author = models.ForeignKey(Profile, related_name="authored_plans")
    description = models.TextField()
    from_date = models.DateField()
    to_date = models.DateField()