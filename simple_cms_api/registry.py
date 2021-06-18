from importlib import import_module

from django.conf import settings as dj_settings

from rest_framework import routers

from .conf import settings
from .models import ThingType
from .utils import import_class


def get_thing_registry():

    if hasattr(dj_settings, settings.GLOBAL_THING_REGISTRY) is True:
        return getattr(dj_settings, settings.GLOBAL_THING_REGISTRY)

    module = import_class(settings.THING_REGISTRY_CLASS)

    return module()


class BaseThingRegistry:

    things = {}

    def __init__(self, router=None):
        self.router = self.set_router(router)

        self.load_things()

        if hasattr(dj_settings, settings.GLOBAL_THING_REGISTRY) is False:
            setattr(dj_settings, settings.GLOBAL_THING_REGISTRY, self)

    @property
    def urls(self):
        return self.router.urls

    def set_router(self, router):

        if router is None:
            return routers.SimpleRouter()

        if type(router, type) is False:
            return router()

        return router

    def load_things(self):

        for module in settings.THING_CLASSES:

            try:
                module = import_class(module)
            except ImportError as e:
                raise ImportError(e.msg)

            instance = module()
            codename = instance.codename

            self.things[codename] = instance

            if instance.has_endpoint is True:
                self.router.register(
                    rf'{codename}',
                    instance.get_viewset(),
                    basename=f'{codename}'
                )

            thing_type = ThingType.objects.filter(
                codename=codename
            ).first()

            if thing_type is None:
                ThingType.objects.create(
                    codename=codename,
                    is_active=True
                )

            else:
                thing_type.is_active = True
                thing_type.save()

        db_thing_type_codenames = ThingType.objects.all().values_list(
            'codename',
            flat=True
        )

        for codename in db_thing_type_codenames:

            if codename not in self.things.keys():

                thing_type = ThingType.objects.filter(
                    codename=codename
                ).first()

                if thing_type is not None:
                    thing_type.is_active = False
                    thing_type.save()

    def get_thing_instance(self, codename):

        try:
            instance = self.things[codename]
        except KeyError as e:
            raise ValueError(
                _(f'Thing with codename "{codename}" does not exist.')
            )

        return instance

    def get_serializer_class(self, codename):
        instance = self.get_thing_instance(codename)
        return instance.get_serializer_class()

    def get_viewset(self, codename):
        instance = self.get_thing_instance(codename)
        return instance.get_viewset()


class ThingRegistry(BaseThingRegistry):
    pass
