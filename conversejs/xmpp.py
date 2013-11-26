#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    Inicial version taken from:

    SleekXMPP: The Sleek XMPP Library
    Copyright (C) 2010  Nathanael C. Fritz

    Modifications by django-conversejs authors.

"""

import sys
import logging

import sleekxmpp
from sleekxmpp.exceptions import IqError, IqTimeout
from dns.resolver import NoNameservers


# Get a logger
logger = logging.getLogger('conversejs.register')


# Python versions before 3.0 do not use UTF-8 encoding
# by default. To ensure that Unicode is handled properly
# throughout SleekXMPP, we will set the default encoding
# ourselves to UTF-8.
if sys.version_info < (3, 0):
    from sleekxmpp.util.misc_ops import setdefaultencoding
    setdefaultencoding('utf8')


TIMEOUT = 10


def register(client, username, password, name, email):
    iq = client.Iq()
    iq['type'] = 'set'
    iq['register']['username'] = username
    iq['register']['password'] = password
    iq['register']['name'] = name
    iq['register']['email'] = email
    iq.send(now=True) #, timeout=TIMEOUT)


def registration_wrapper(client, function, logger_success, logger_error,
                         use_client, args, kwargs):

    connected = client.connect(reattempt=False)

    if not connected:
        logger.error('Unable to connect to XMPP server.')
        return False

    client.process()

    success = False
    try:
        if use_client:
            function(client, *args, **kwargs)
        else:
            function(*args, **kwargs)
        logger.info(logger_success % client.boundjid)
        success = True
    except IqError as e:
        logger.error(logger_error % e.iq['error']['text'])
    except IqTimeout:
        logger.error("No response from server.")
    finally:
        client.disconnect()
    return success


def register_account(jid, password, name='', email=''):
    client = sleekxmpp.ClientXMPP(jid, password)
    client.register_plugin('xep_0077') # In-band Registration

    registration_wrapper(
        client=client,
        function=register,
        logger_success="Account created for %s!",
        logger_error="Could not register account: %s",
        use_client=True,
        args=[client.boundjid.user, password, name, email],
        kwargs={}
    )


def change_password(jid, old_password, new_password):
    client = sleekxmpp.ClientXMPP(jid, old_password)
    client.register_plugin('xep_0077') # In-band Registration

    registration_wrapper(
        client=client,
        function=client['xep_0077'].change_password,
        logger_success="Password changed for %s!",
        logger_error="Could not change password for account: %s",
        use_client=False,
        args=[new_password, client.boundjid.server, client.boundjid.bare],
        kwargs=dict(timeout=TIMEOUT)
    )
