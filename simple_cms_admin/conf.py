from django.conf import settings as dj_settings


class Settings:

    GLOBAL_THING_CLASSES = 'SIMPLE_CMS_ADMIN_THING_CLASSES'
    GLOBAL_THING_REGISTRY_CLASS = 'SIMPLE_CMS_ADMIN_THING_REGISTRY_CLASS'
    GLOBAL_THING_REGISTRY = 'SIMPLE_CMS_ADMIN_THING_REGISTRY'

    ADMIN_THINGS_EDIT_URLNAME = 'admin-things-edit'
    ADMIN_THINGS_LIST_URLNAME = 'admin-things-list'

    ADMIN_HOME_URLNAME = ADMIN_THINGS_LIST_URLNAME

    def __init__(self):
        pass

    @property
    def THING_CLASSES(self):
        return getattr(
            dj_settings,
            settings.GLOBAL_THING_CLASSES,
            []
        )

    @property
    def THING_REGISTRY_CLASS(self):
        return getattr(
            dj_settings,
            self.GLOBAL_THING_REGISTRY_CLASS,
            'simple_cms_admin.registry.ThingRegistry'
        )

    def __getattr__(self, name):
        return getattr(dj_settings, name, None)


settings = Settings()
