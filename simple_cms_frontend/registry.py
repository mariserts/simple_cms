from importlib import import_module

from django.conf import settings as dj_settings
from django.urls import path
from django.utils.translation import gettext_lazy as _

from .conf import settings
from .things import Thing
from .utils import import_class


def get_thing_registry():

    if hasattr(dj_settings, settings.GLOBAL_THING_REGISTRY) is True:
        return getattr(dj_settings, settings.GLOBAL_THING_REGISTRY)

    module = import_class(settings.THING_REGISTRY_CLASS)

    return module()


class BaseThingRegistry:

    things = {}
    default_thing_type = Thing
    urlpatterns = []

    def __init__(self):

        self.load_things()

        if hasattr(dj_settings, settings.GLOBAL_THING_REGISTRY) is False:
            setattr(dj_settings, settings.GLOBAL_THING_REGISTRY, self)

    def load_things(self):

        for module in settings.THING_CLASSES:

            try:
                module = import_class(module)
            except ImportError as e:
                raise ImportError(e.msg)

            instance = module()
            codename = instance.codename

            self.things[codename] = instance

            if instance.urlpattern is not None:
                self.urlpatterns.append(instance.urlpattern)

    def get_thing_instance(self, codename):

        try:
            instance = self.things[codename]
        except KeyError as e:
            instance = self.default_thing_type()

        return instance

    def get_serializer_class(self, codename):
        instance = self.get_thing_instance(codename)
        return instance.get_serializer_class()

    def get_form_class(self, codename):
        instance = self.get_thing_instance(codename)
        return instance.get_form_class()


class ThingRegistry(BaseThingRegistry):
    pass
