from django.conf import settings as dj_settings


class Settings:

    RELATED_NAME_SITE_TENANT = 'sites'
    RELATED_NAME_THING_TENANT = 'things'
    RELATED_NAME_THING_THING_TYPE = 'things'
    RELATED_NAME_THINGVECTOR_THING = 'vectors'
    RELATED_NAME_TENANT_DESCRIBED_BY = 'tenant_description'
    RELATED_NAME_TENANT_PARENT = 'sub_tenants'
    RELATED_NAME_TENANTUSER_TENANT = 'users'
    RELATED_NAME_TENANTUSER_USER = 'tenants'
    RELATED_NAME_TRANSLATABLE_THING = 'translatables'
    RELATED_NAME_TRANSLATABLEVECTOR_THING = 'translatable_vectors'
    RELATED_NAME_TRANSLATABLEVECTOR_TRANSLATABLE = 'vectors'

    GLOBAL_THING_CLASSES = 'SIMPLE_CMS_API_THING_CLASSES'
    GLOBAL_THING_REGISTRY_CLASS = 'SIMPLE_CMS_API_THING_REGISTRY_CLASS'
    GLOBAL_THING_REGISTRY = 'SIMPLE_CMS_API_THING_REGISTRY'

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
            'simple_cms_api.registry.ThingRegistry'
        )


settings = Settings()
