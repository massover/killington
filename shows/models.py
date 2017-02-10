from django.core.validators import RegexValidator
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.formats import date_format
from django.utils.translation import ugettext_lazy as _

from .managers import ActiveLotteryManager


class Show(models.Model):
    name = models.CharField(max_length=31)
    subscribed_users = models.ManyToManyField('User')

    def __str__(self):
        return '%s' % self.name


class Performance(models.Model):
    show = models.ForeignKey(Show)
    starts_at = models.DateTimeField()

    def __str__(self):
        starts_at = date_format(self.starts_at, 'DATETIME_FORMAT')
        return '%s %s' % (self.show.name, starts_at)


class Lottery(models.Model):
    objects = models.Manager()
    active_objects = ActiveLotteryManager()

    performance = models.OneToOneField(Performance)
    lottery_id = models.IntegerField()
    nonce = models.CharField(max_length=31)
    starts_at = models.DateTimeField()
    processed = models.BooleanField(default=False)
    entered_users = models.ManyToManyField('User')

    class Meta:
        verbose_name_plural = 'Lotteries'

    @property
    def url(self):
        return 'https://lottery.broadwaydirect.com/enter-lottery/?lottery={}&window=popup'.format(
            self.lottery_id
        )

    @property
    def http_referer(self):
        return '/enter-lottery/?lottery={}&window=popup'.format(self.lottery_id)

    def __str__(self):
        starts_at = date_format(self.starts_at, 'DATETIME_FORMAT')
        return '%s %s' % (self.performance.show.name, starts_at)


numeric_validator = RegexValidator(r'^[0-9]*$', _('Only numbers allowed.'))


class User(AbstractUser):
    date_of_birth = models.DateField(_('date of birth'))
    zipcode = models.CharField(_('ZIP code'), max_length=5, validators=[numeric_validator])

    REQUIRED_FIELDS = ['email', 'date_of_birth', 'zipcode']
