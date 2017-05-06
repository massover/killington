from datetime import timedelta
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.conf import settings
from django.core.validators import RegexValidator
from django.db import models
from django.contrib.auth.models import PermissionsMixin, AbstractBaseUser
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.templatetags.static import static
from django.utils import timezone
from django.utils.formats import date_format
from django.utils.translation import ugettext_lazy as _
from django_extensions.db.fields import AutoSlugField

from .managers import (EnterableLotteryManager, UserManager, SESManager,
                       EnterableFloodManager,)

from . import utils


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


class User(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=30, blank=True)
    email = models.EmailField(_('email address'), unique=True)
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this admin site.'),
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
    date_of_birth = models.DateField(_('date of birth'))
    zipcode = models.CharField(_('ZIP code'), max_length=5, validators=[numeric_validator])

    is_confirmed = models.BooleanField(default=False)
    confirmation_code = models.CharField(max_length=32, default=utils.generate_confirmation_code)

    objects = UserManager()

    REQUIRED_FIELDS = ['date_of_birth', 'zipcode']
    USERNAME_FIELD = 'email'

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def get_full_name(self):
        """
        Returns the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        "Returns the short name for the user."
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        """
        Sends an email to this User.
        """
        send_mail(subject, message, from_email, [self.email], **kwargs)


class SES(models.Model):
    EMAIL_LENGTH = 32

    objects = SESManager()

    email = models.EmailField(unique=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='ses_set')

    class Meta:
        verbose_name = 'SES'
        verbose_name_plural = 'SES Set'
        ordering = ('id', )

    def __str__(self):
        return self.email


class Flood(models.Model):
    objects = models.Manager()
    enterable_objects = EnterableFloodManager()

    lottery = models.ForeignKey(Lottery)
    client = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='client_floods')
    manager = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='manager_floods')
    entered_ses_set = models.ManyToManyField(SES, blank=True)

    def generate_users(self):
        for index, ses in enumerate(self.client.ses_set.all()):
            yield User(
                first_name=self.client.first_name,
                last_name=self.client.last_name,
                zipcode=self.client.zipcode,
                email=ses.email,
                date_of_birth=self.client.date_of_birth + timedelta(days=index),
            )

    def __str__(self):
        return str(self.id)
