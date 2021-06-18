from django.shortcuts import reverse
from django.utils.translation import gettext_lazy as _

from .conf import settings
from .forms import ThingForm
from .serializers import ThingSerializer


class BaseThing:

    codename = 'things'
    name = _('Thing')
    name_plural = _('Things')
    serializer_class = None
    form_class = None
    urlpattern = None

    def __init__(self):
        pass

    def get_form_class(self):
        return self.form_class or ThingForm

    def get_serializer_class(self):
        return self.serializer_class or ThingSerializer

    def get_urlpattern(self):
        return self.urlpattern

    def get_edit_page_url(self, data):
        return reverse(
            settings.ADMIN_THINGS_EDIT_URLNAME,
            kwargs={
                'tenant_id': data['tenant']['id'],
                'codename': data['thing_type']['codename'],
                'pk': data['id']
            }
        )


class Thing(BaseThing):
    pass
