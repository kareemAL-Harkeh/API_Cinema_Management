from django.db import models

from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.conf import settings


class Movie(models.Model) :
    hall = models.CharField(max_length=30)
    movie = models.CharField(max_length=30)
    #date = models.DateField()


class Guest(models.Model) :
    name = models.CharField(max_length=30)
    mobile = models.CharField(max_length=30)


class Reservation(models.Model) :
    guest = models.ForeignKey(Guest , related_name='reservation' ,on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie , related_name='reservation' ,on_delete=models.CASCADE)

@receiver(post_save, sender = settings.AUTH_USER_MODEL)
def TokenCreate(sender, instance, created, **kwagrs):
    if created:
        Token.objects.create(user= instance)
