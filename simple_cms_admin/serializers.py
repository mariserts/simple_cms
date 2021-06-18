from django.conf import settings as dj_settings
from django.shortcuts import reverse
from django.utils import dateparse
from django.utils.translation import gettext_lazy as _

from .clients.things.client import ThingDetailClient, ThingListClient
from .conf import settings
from .utils import get_thing_url


class ThingSerializerApiMixin:

    @staticmethod
    def create(self, request=None, *args, **kwrags):
        pass

    @staticmethod
    def destroy(self, request=None, *args, **kwrags):
        pass

    @staticmethod
    def update(request, tenant_id, codename, pk, data):
        return ThingDetailClient().update(tenant_id, codename, pk, data)

    @staticmethod
    def retrieve(request, tenant_id, codename, pk):
        return ThingDetailClient().get(tenant_id, codename, pk)

    @staticmethod
    def list(
            request=None,
            page=1,
            page_size=10,
            tenant_id=None,
            codename=None,
            q=None,
            *args,
            **kwargs):

        return ThingListClient().get(page=page, page_size=page_size)


class Serializer:

    def __init__(self, objects, many=False):
        self.objects = self.normalize_objects(objects)
        self.many = many

    @property
    def data(self):
        for object in self.objects:
            object = self.format_object(object)
        return self._many(self.objects)

    def format_object(object):
        return object

    def normalize_objects(self, objects):

        if isinstance(objects, dict) is True:
            return [objects]

        if isinstance(objects, list) is False:
            raise ValueError(_('Objects must be of type dict or list'))

        return objects

    def _many(self, data):

        if self.many is True:
            return data

        return next(iter(data), None)


class ThingSerializer(ThingSerializerApiMixin, Serializer):

    @property
    def data(self):

        for object in self.objects:
            object['admin_display'] = self.get_admin_display_data(object)

        return self._many(self.objects)

    def get_admin_display_data(self, object):

        default_language = dj_settings.DEFAULT_CONTENT_LANGUAGE[0]

        codename = object.get('thing_type', {}).get('codename', {})
        created_at = object.get('created_at')
        tenant = object.get('tenant', {}).get('system_name', None)
        translatables = object.get('translatables', [])

        registry = getattr(
            dj_settings,
            settings.GLOBAL_THING_REGISTRY,
            None
        )

        thing_instance = registry.get_thing_instance(codename)

        data = {
            'title': None,
            'url': thing_instance.get_edit_page_url(object),
            'codename': codename,
            'created_at': dateparse.parse_datetime(created_at),
            'tenant': tenant,
        }

        for translatable in translatables:
            if translatable.get('language', None) == default_language:
                data['title'] = translatable['title']

        if data['title'] is None:
            data['title'] = f'Thing ID-{object["id"]}'

        return data
