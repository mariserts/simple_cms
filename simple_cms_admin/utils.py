from importlib import import_module

from django.shortcuts import reverse

from .conf import settings


def import_class(string):

    parts = string.split('.')

    cls = parts.pop()

    module = import_module('.'.join(parts))

    return getattr(module, cls)


def get_admin_home_url():
    return reverse(settings.ADMIN_HOME_URLNAME)


def get_thing_url(thing_dict):
    return reverse(
        settings.ADMIN_THINGS_EDIT_URLNAME,
        kwargs={
            'tenant_id': thing_dict['tenant']['id'],
            'codename': thing_dict['thing_type']['codename'],
            'pk': thing_dict['id']
        }
    )
