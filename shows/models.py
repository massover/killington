from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.templatetags.static import static
from django.utils import timezone
from django.utils.formats import date_format
from django.utils.translation import ugettext_lazy as _
from django_extensions.db.fields import AutoSlugField

from .managers import EnterableLotteryManager


class Show(models.Model):
    name = models.CharField(max_length=31)
    slug = AutoSlugField(populate_from='name')
    subscribed_users = models.ManyToManyField('User',
                                              related_name='subscribed_shows',
                                              blank=True)
    url = models.URLField()

    @property
    def img(self):
        return static('shows/images/{}.jpg'.format(self.slug))

    def __str__(self):
        return '%s' % self.name


class Performance(models.Model):
    show = models.ForeignKey(Show)
    starts_at = models.DateTimeField()

    def __str__(self):
        starts_at = date_format(self.starts_at, 'DATETIME_FORMAT', use_l10n=True)
        return '%s %s' % (self.show.name, starts_at)


@receiver(post_save, sender=Performance)
def performance_post_save(sender, instance, created, **kwargs):
    if created:
        Lottery.objects.create(performance=instance)


class Lottery(models.Model):
    ACTIVE_STATE = 'active'
    PENDING_STATE = 'pending'
    CLOSED_STATE = 'closed'
    INVALID_STATE = 'invalid'

    objects = models.Manager()
    enterable_objects = EnterableLotteryManager()

    performance = models.OneToOneField('Performance')
    external_performance_id = models.IntegerField(blank=True, null=True)
    nonce = models.CharField(max_length=31, blank=True, null=True)
    starts_at = models.DateTimeField(blank=True, null=True)
    ends_at = models.DateTimeField(blank=True, null=True)
    entered_users = models.ManyToManyField('User',
                                           related_name='entered_lotteries',
                                           blank=True)

    class Meta:
        verbose_name_plural = 'Lotteries'

    def clean(self):
        if self.ends_at is None:
            return

        if self.starts_at > self.ends_at:
            raise ValidationError(_('Starts at time must begin before ends at time'))

        if self.starts_at == self.ends_at:
            raise ValidationError(_('Starts at time cannot equal ends at time'))

    @property
    def state(self):
        if timezone.now() < self.starts_at:
            return self.PENDING_STATE
        elif self.starts_at <= timezone.now() and self.ends_at is None:
            return self.INVALID_STATE
        elif self.starts_at <= timezone.now() < self.ends_at:
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
