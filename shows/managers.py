from django.conf import settings
from django.contrib.auth.base_user import BaseUserManager
from django.db import models
from django.utils import timezone
from django.utils.crypto import get_random_string


class EnterableFloodManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(
            lottery__starts_at__lte=timezone.now(),
            lottery__ends_at__gt=timezone.now(),
            lottery__nonce__isnull=False,
            lottery__external_performance_id__isnull=False,
            entered_ses_set=None,
        )


class EnterableLotteryManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(
            starts_at__lte=timezone.now(),
            ends_at__gt=timezone.now(),
            nonce__isnull=False,
            external_performance_id__isnull=False,
        )


class SESManager(models.Manager):
    def bulk_create_with_random_emails_for_user(self, user, num_objects=1000):
        ses_set = []
        for _ in range(num_objects):
            email = '{random_string}@{ses_domain}'.format(
                random_string=get_random_string(length=self.model.EMAIL_LENGTH),
                ses_domain=settings.SES_DOMAIN
            )
            ses_set.append(self.model(user=user, email=email))

        self.bulk_create(ses_set)


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """
        Creates and saves a User with the given username, email and password.
        """
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)

    def get_by_natural_key(self, username):
        username_field_iexact = '{}__iexact'.format(self.model.USERNAME_FIELD)
        return self.get(**{username_field_iexact: username})