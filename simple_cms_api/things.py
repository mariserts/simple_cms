from django.utils.translation import gettext_lazy as _

from .serializers import ThingSerializer
from .viewsets.things.public import PublicThingViewset


class BaseThing:

    codename = 'things'
    has_endpoint = False
    name = _('Thing')
    name_plural = _('Things')
    serializer_class = None
    viewset = None

    def __init__(self):
        pass

    def get_serializer_class(self):
        return self.serializer_class or ThingSerializer

    def get_viewset(self):
        return self.viewset or PublicThingViewset


class Thing(BaseThing):
    pass
