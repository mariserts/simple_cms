from django.contrib import admin
from django.urls import path

from .conf import settings
from .registry import get_thing_registry


urlpatterns = []


registry = get_thing_registry()


if len(registry.urlpatterns) != 0:
    urlpatterns += registry.urlpatterns
