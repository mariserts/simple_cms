from django.urls import path

from simple_cms_admin.things import BaseThing

from .conf import settings
from .viewsets.things.edit import TenantThingDetailView


class TenantThing(BaseThing):

    codename = settings.CODENAME
    name = settings.NAME
    name_plural = settings.NAME_PLURAL
    serializer_class = None
    form_class = None
    urlpattern = path(
        rf'admin/<str:tenant_id>/{codename}/<str:pk>/',
        TenantThingDetailView.as_view(),
        name=settings.URL_NAME_EDIT_PAGE
    )
