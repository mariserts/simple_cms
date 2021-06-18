from django.utils.translation import gettext_lazy as _


class Settings:

    CODENAME = 'tenants'

    NAME = _('Tenant')
    NAME_PLURAL = _('Tentants')

    URL_NAME_EDIT_PAGE = 'edit-tenant'


settings = Settings()
