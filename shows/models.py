from django.core.validators import RegexValidator
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _


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


numeric_validator = RegexValidator(r'^[0-9]*$', _('Only numbers allowed.'))

class User(AbstractUser):
    date_of_birth = models.DateTimeField(_('date of birth'))
    zipcode = models.CharField(_('ZIP code'), max_length=5, validators=[numeric_validator])

    REQUIRED_FIELDS = ['email', 'date_of_birth', 'zipcode']
