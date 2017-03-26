from django.contrib.auth.base_user import BaseUserManager
from django.db import models
from django.utils import timezone


class EnterableLotteryManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(
            starts_at__lte=timezone.now(),
            ends_at__gt=timezone.now(),
            nonce__isnull=False,
            external_performance_id__isnull=False,
        )


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