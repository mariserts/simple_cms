# -*- coding: utf-8 -*-
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from . import models
from .forms import UserCreationForm, UserChangeForm


class TenantAdmin(admin.ModelAdmin):
    models = models.Tenant
    raw_id_fields = ['described_by', 'parent']


class TranslatableInline(admin.TabularInline):
    extra = 0
    model = models.Translatable
    raw_id_fields = ['thing', ]


class TranslatableVectorAdmin(admin.ModelAdmin):
    models = models.TranslatableVector
    raw_id_fields = ['thing', 'translatable']


class ThingAdmin(admin.ModelAdmin):
    inlines = [TranslatableInline, ]
    models = models.Thing
    raw_id_fields = ['tenant', ]


class ThingVectorAdmin(admin.ModelAdmin):
    models = models.ThingVector
    raw_id_fields = ['thing', ]


class UserAdmin(UserAdmin):
    add_form = UserCreationForm
    form = UserChangeForm
    model = models.User
    list_display = (
        'email',
        'is_staff',
        'is_active',
    )
    list_filter = (
        'email',
        'is_staff',
        'is_active',
    )
    fieldsets = (
        (
            None,
            {
                'fields': (
                    'email',
                    'password'
                )
            }
        ),
        (
            'Permissions',
            {
                'fields': (
                    'is_staff',
                    'is_active',
                    'is_superuser',
                )
            }
        ),
    )
    add_fieldsets = (
        (
            None, {
                'classes': (
                    'wide',
                ),
                'fields': (
                    'email',
                    'password1',
                    'password2',
                    'is_staff',
                    'is_active',
                    'is_superuser',
                )
            }
        ),
    )
    search_fields = (
        'email',
    )
    ordering = (
        'email',
    )


admin.site.register(models.Tenant, TenantAdmin)
admin.site.register(models.Thing, ThingAdmin)
admin.site.register(models.ThingVector, ThingVectorAdmin)
admin.site.register(models.TranslatableVector, TranslatableVectorAdmin)
admin.site.register(models.User, UserAdmin)
