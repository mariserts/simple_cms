# -*- coding: utf-8 -*-
from django import template
from django.conf import settings as dj_settings
from django.shortcuts import reverse
from django.utils.translation import gettext_lazy as _

from ..conf import settings


register = template.Library()


FOOTER_TEMPLATE = 'simple_cms_admin/components/navbars/footer.html'
MAIN_MENU_TEMPLATE = 'simple_cms_admin/components/navbars/mainmenu.html'


@register.inclusion_tag(MAIN_MENU_TEMPLATE, takes_context=True)
def main_menu(context):

    home_url = reverse(settings.ADMIN_HOME_URLNAME)

    return {
        'project_title': dj_settings.PROJECT_TITLE,
        'home_link': home_url,
        'links': [
            {
                'items': [],
                'title': _('Home'),
                'url': home_url,
            },
            {
                'items': [],
                'title': _('Sign out'),
                'url': '#',
            }
        ]
    }


@register.inclusion_tag(FOOTER_TEMPLATE, takes_context=True)
def footer(context):
    return {}
