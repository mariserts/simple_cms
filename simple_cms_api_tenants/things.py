from django.utils.translation import gettext_lazy as _

from simple_cms_api.things import BaseThing

from .serializers import TenantSerializer


class TenantThing(BaseThing):

    codename = 'tenants'
    has_endpoint = True
    name = _('Tentant')
    name_plural = _('Tentants')
    serializer_class = TenantSerializer
    viewset = None
