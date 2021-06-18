import uuid

from django.conf import settings as dj_settings
from django.contrib.auth.models import AbstractUser
from django.contrib.postgres.search import SearchVectorField
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _

from .conf import settings
from .managers import UserManager


INDEX_WEIGHT_CHOICES = [
    ['A', 'A'],
    ['B', 'B'],
    ['C', 'C'],
    ['D', 'D'],
    ['E', 'E'],
]


# Mixins

class DateTimeStampedFieldMixin(models.Model):

    class Meta:
        abstract = True

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class UuidStampedFieldMixin(models.Model):

    class Meta:
        abstract = True

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        unique=True
    )


# Models

class ThingType(
        DateTimeStampedFieldMixin,
        UuidStampedFieldMixin,
        models.Model):

    codename = models.CharField(max_length=255, unique=True)
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.codename


class Thing(
        DateTimeStampedFieldMixin,
        UuidStampedFieldMixin,
        models.Model):

    tenant = models.ForeignKey(
        'Tenant',
        on_delete=models.CASCADE,
        related_name=settings.RELATED_NAME_THING_TENANT
    )
    thing_type = models.ForeignKey(
        'ThingType',
        on_delete=models.CASCADE,
        related_name=settings.RELATED_NAME_THING_THING_TYPE
    )

    data = models.JSONField(default=dict, blank=True)

    is_deleted = models.BooleanField(default=False)
    is_published = models.BooleanField(default=False)

    archive_at = models.DateTimeField(blank=True, null=True)
    publish_at = models.DateTimeField(blank=True, null=True)


class Translatable(
        DateTimeStampedFieldMixin,
        UuidStampedFieldMixin,
        models.Model):

    thing = models.ForeignKey(
        Thing,
        on_delete=models.CASCADE,
        related_name=settings.RELATED_NAME_TRANSLATABLE_THING
    )

    data = models.JSONField(default=dict, blank=True)
    language = models.CharField(max_length=255, choices=dj_settings.LANGUAGES)


# Search vectors

class ThingVector(
        DateTimeStampedFieldMixin,
        UuidStampedFieldMixin,
        models.Model):

    thing = models.ForeignKey(
        Thing,
        on_delete=models.CASCADE,
        related_name=settings.RELATED_NAME_THINGVECTOR_THING
    )

    field_name = models.CharField(max_length=255, db_index=True)
    raw_value = models.TextField(blank=True, null=True)
    vector = SearchVectorField()
    weight = models.CharField(max_length=255, choices=INDEX_WEIGHT_CHOICES)


class TranslatableVector(
        DateTimeStampedFieldMixin,
        UuidStampedFieldMixin,
        models.Model):

    thing = models.ForeignKey(
        Thing,
        on_delete=models.CASCADE,
        related_name=settings.RELATED_NAME_TRANSLATABLEVECTOR_THING
    )
    translatable = models.ForeignKey(
        Translatable,
        on_delete=models.CASCADE,
        related_name=settings.RELATED_NAME_TRANSLATABLEVECTOR_TRANSLATABLE
    )

    field_name = models.CharField(max_length=255, db_index=True)
    raw_value = models.TextField(blank=True, null=True)
    vector = SearchVectorField()
    weight = models.CharField(max_length=255, choices=INDEX_WEIGHT_CHOICES)


# Tenancy

class Tenant(
        DateTimeStampedFieldMixin,
        UuidStampedFieldMixin,
        models.Model):

    parent = models.ForeignKey(
        'Tenant',
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name=settings.RELATED_NAME_TENANT_PARENT,
    )

    described_by = models.ForeignKey(
        Thing,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name=settings.RELATED_NAME_TENANT_DESCRIBED_BY
    )
    system_name = models.CharField(max_length=255)
    has_subtenant_content = models.BooleanField(default=False)

    is_active = models.BooleanField(default=False)
    is_archived = models.BooleanField(default=False)

    def __str__(self):
        return self.system_name


class User(
    AbstractUser,
    UuidStampedFieldMixin):

    email = models.EmailField(unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def save(self, *args, **kwargs):

        if self.email in [None, '', ' ']:
            raise ValidationError(_('User must have email'))

        self.username = self.email

        super(User, self).save(*args, **kwargs)


class TenantUser(
        DateTimeStampedFieldMixin,
        UuidStampedFieldMixin,
        models.Model):

    class Meta:
        unique_together = (
            'tenant',
            'user'
        )

    tenant = models.ForeignKey(
        Tenant,
        on_delete=models.CASCADE,
        related_name=settings.RELATED_NAME_TENANTUSER_TENANT
    )
    user = models.ForeignKey(
        dj_settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name=settings.RELATED_NAME_TENANTUSER_USER
    )


class Site(
        DateTimeStampedFieldMixin,
        UuidStampedFieldMixin,
        models.Model):

    tenant = models.ForeignKey(
        Tenant,
        on_delete=models.CASCADE,
        related_name=settings.RELATED_NAME_SITE_TENANT
    )

    domain = models.CharField(max_length=255, unique=True, db_index=True)

    is_active = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        self.domain = self.clean_domain(self.domain)
        super().save(*args, **kwargs)

    @staticmethod
    def clean_domain(domain):
        return domain
