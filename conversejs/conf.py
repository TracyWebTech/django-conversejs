from django.conf import settings


# Django-conversejs settings
CONVERSEJS_AUTO_REGISTER = getattr(settings, 'CONVERSEJS_AUTO_REGISTER', False)
CONVERSEJS_ENABLED = getattr(settings, 'CONVERSEJS_ENABLED', True)


def get_conversejs_settings():
    """This helper function returns all the configuration needed by
    Converse.js frontend (javascript).

    Configurations specific to django-conversejs should be added above.

    """
    converse_settings = {
        'CONVERSEJS_AUTO_LIST_ROOMS': False,
        'CONVERSEJS_AUTO_SUBSCRIBE': False,
        'CONVERSEJS_BOSH_SERVICE_URL': 'https://bind.opkode.im',
        'CONVERSEJS_HIDE_MUC_SERVER': False,
        'CONVERSEJS_PREBIND': True,
        'CONVERSEJS_SHOW_CONTROLBOX_BY_DEFAULT': False,
        'CONVERSEJS_XHR_USER_SEARCH': False,
        'CONVERSEJS_DEBUG': settings.DEBUG,
        'CONVERSEJS_SHOW_ONLY_ONLINE_USERS': False,
        'CONVERSEJS_ALLOW_CONTACT_REQUESTS': True,
    }

    for key, value in converse_settings.items():
        conf = getattr(settings, key, value)

        if isinstance(conf, bool):
            conf = unicode(conf).lower()

        converse_settings[key] = conf

    return converse_settings

