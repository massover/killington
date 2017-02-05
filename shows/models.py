from django.db import models
from django.contrib.auth.models import AbstractUser


class Show(models.Model):
    name = models.CharField(max_length=255)


class ShowTime(models.Model):
    show = models.ForeignKey(Show)
    starts_at = models.DateTimeField()

    class Meta:
        verbose_name = 'Show Time'


class Lottery(models.Model):
    show = models.ForeignKey(Show)
    lottery_id = models.IntegerField()
    nonce = models.CharField(max_length=31)
    starts_at = models.DateTimeField()

    class Meta:
        verbose_name_plural = 'Lotteries'


class User(AbstractUser):
    pass