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
import getpass
from optparse import OptionParser

import sleekxmpp
from sleekxmpp.exceptions import IqError, IqTimeout


# Get a logger
logger = logging.getLogger('conversejs.register')


# Python versions before 3.0 do not use UTF-8 encoding
# by default. To ensure that Unicode is handled properly
# throughout SleekXMPP, we will set the default encoding
# ourselves to UTF-8.
if sys.version_info < (3, 0):
    from sleekxmpp.util.misc_ops import setdefaultencoding
    setdefaultencoding('utf8')
else:
    raw_input = input


class RegisterBot(sleekxmpp.ClientXMPP):

    """
    A basic bot that will attempt to register an account
    with an XMPP server.

    NOTE: This follows the very basic registration workflow
          from XEP-0077. More advanced server registration
          workflows will need to check for data forms, etc.
    """

    def __init__(self, jid, password, name=None, email=None):
        sleekxmpp.ClientXMPP.__init__(self, jid, password)

        self.name = name
        self.email = email

        # The session_start event will be triggered when
        # the bot establishes its connection with the server
        # and the XML streams are ready for use. We want to
        # listen for this event so that we we can initialize
        # our roster.
        self.add_event_handler("session_start", self.start, threaded=True)

        # The register event provides an Iq result stanza with
        # a registration form from the server. This may include
        # the basic registration fields, a data form, an
        # out-of-band URL, or any combination. For more advanced
        # cases, you will need to examine the fields provided
        # and respond accordingly. SleekXMPP provides plugins
        # for data forms and OOB links that will make that easier.
        self.add_event_handler("register", self.register, threaded=True)

    def start(self, event):
        """
        Process the session_start event.

        Typical actions for the session_start event are
        requesting the roster and broadcasting an initial
        presence stanza.

        Arguments:
            event -- An empty dictionary. The session_start
                     event does not provide any additional
                     data.
        """
        self.send_presence()
        self.get_roster()

        # We're only concerned about registering, so nothing more to do here.
        self.disconnect()

    def register(self, iq):
        """
        Fill out and submit a registration form.

        The form may be composed of basic registration fields, a data form,
        an out-of-band link, or any combination thereof. Data forms and OOB
        links can be checked for as so:

        if iq.match('iq/register/form'):
            # do stuff with data form
            # iq['register']['form']['fields']
        if iq.match('iq/register/oob'):
            # do stuff with OOB URL
            # iq['register']['oob']['url']

        To get the list of basic registration fields, you can use:
            iq['register']['fields']
        """

        resp = self.Iq()
        resp['type'] = 'set'
        resp['register']['username'] = self.boundjid.user
        resp['register']['password'] = self.password

        if self.name:
            resp['register']['name'] = self.name

        if self.email:
            resp['register']['email'] = self.email

        # TODO: Raise exception if fails
        try:
            resp.send(now=True)
            logger.info("Account created for %s!" % self.boundjid)
        except IqError as e:
            logger.error("Could not register account: %s" %
                    e.iq['error']['text'])
            self.disconnect()
        except IqTimeout:
            logger.error("No response from server.")
            self.disconnect()


def register_account(jid, password, name=None, email=None):
    # Setup the RegisterBot and register plugins. Note that while plugins may
    # have interdependencies, the order in which you register them does
    # not matter.
    xmpp = RegisterBot(jid, password, name, email)
    xmpp.register_plugin('xep_0030') # Service Discovery
    xmpp.register_plugin('xep_0004') # Data forms
    xmpp.register_plugin('xep_0066') # Out-of-band Data
    xmpp.register_plugin('xep_0077') # In-band Registration

    # Some servers don't advertise support for inband registration, even
    # though they allow it. If this applies to your server, use:
    xmpp['xep_0077'].force_registration = True

    # If you are working with an OpenFire server, you may need
    # to adjust the SSL version used:
    # xmpp.ssl_version = ssl.PROTOCOL_SSLv3

    # If you want to verify the SSL certificates offered by a server:
    # xmpp.ca_certs = "path/to/ca/cert"

    # Connect to the XMPP server and start processing XMPP stanzas.
    if xmpp.connect():
        xmpp.process(block=True)
    else:
        logger.error('Unable to connect to XMPP server.')
        return False

    return True
