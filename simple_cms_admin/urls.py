from django.contrib import admin
from django.urls import path

from .conf import settings
from .registry import get_thing_registry
from .viewsets.things.edit import ThingDetailView
from .viewsets.things.list import ThingListView


urlpatterns = []


registry = get_thing_registry()


if len(registry.urlpatterns) != 0:
    urlpatterns += registry.urlpatterns


urlpatterns += [
    path(
        'admin/<str:tenant_id>/<str:codename>/<str:pk>/',
        ThingDetailView.as_view(),
        name=settings.ADMIN_THINGS_EDIT_URLNAME
    ),
    path(
        'admin/',
        ThingListView.as_view(),
        name=settings.ADMIN_THINGS_LIST_URLNAME
    )
]
