from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.utils.formats import date_format
from django.utils.translation import ugettext_lazy as _

from .managers import ActiveLotteryManager


class Show(models.Model):
    name = models.CharField(max_length=31)
    subscribed_users = models.ManyToManyField('User', blank=True)
    url = models.URLField()

    def __str__(self):
        return '%s' % self.name


class Performance(models.Model):
    show = models.ForeignKey(Show)
    starts_at = models.DateTimeField()

    def __str__(self):
        starts_at = date_format(self.starts_at, 'DATETIME_FORMAT', use_l10n=True)
        return '%s %s' % (self.show.name, starts_at)


class Lottery(models.Model):
    ACTIVE_STATE = 'active'
    PENDING_STATE = 'pending'
    CLOSED_STATE = 'closed'

    objects = models.Manager()
    active_objects = ActiveLotteryManager()

    performance = models.OneToOneField(Performance)
    external_performance_id = models.IntegerField(blank=True, null=True)
    nonce = models.CharField(max_length=31, blank=True, null=True)
    starts_at = models.DateTimeField(blank=True, null=True)
    ends_at = models.DateTimeField(blank=True, null=True)
    processed = models.BooleanField(default=False)
    entered_users = models.ManyToManyField('User', blank=True)

    class Meta:
        verbose_name_plural = 'Lotteries'

    def clean(self):
        if self.starts_at > self.ends_at:
            raise ValidationError(_('Starts at time must begin before ends at time'))

        if self.starts_at == self.ends_at:
            raise ValidationError(_('Starts at time cannot equal ends at time'))

    @property
    def state(self):
        if timezone.now() < self.starts_at:
            return self.PENDING_STATE
        if self.starts_at <= timezone.now() < self.ends_at:
            return self.ACTIVE_STATE
        else:
            return self.CLOSED_STATE

    @property
    def url(self):
        return 'https://lottery.broadwaydirect.com/enter-lottery/?lottery={}&window=popup'.format(
            self.external_performance_id
        )

    @property
    def http_referer(self):
        return '/enter-lottery/?lottery={}&window=popup'.format(self.external_performance_id)

    def __str__(self):
        starts_at = date_format(self.starts_at, 'DATETIME_FORMAT', use_l10n=True)
        return '%s %s' % (self.performance.show.name, starts_at)


numeric_validator = RegexValidator(r'^[0-9]*$', _('Only numbers allowed.'))


class User(AbstractUser):
    date_of_birth = models.DateField(_('date of birth'))
    zipcode = models.CharField(_('ZIP code'), max_length=5, validators=[numeric_validator])

    REQUIRED_FIELDS = ['email', 'date_of_birth', 'zipcode']
