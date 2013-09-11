"""
BOSH Client
-----------

Based on https://friendpaste.com/1R4PCcqaSWiBsveoiq3HSy

"""

import base64
import httplib
import logging

from random import randint
from urlparse import urlparse
from xml.etree import ElementTree as ET

from puresasl.client import SASLClient 


HTTPBIND_NS = 'http://jabber.org/protocol/httpbind'
BOSH_NS = 'urn:xmpp:xbosh'
XMPP_SASL_NS = 'urn:ietf:params:xml:ns:xmpp-sasl'
XMPP_BIND_NS = 'urn:ietf:params:xml:ns:xmpp-bind'
JABBER_CLIENT_NS = 'jabber:client'
JABBER_STREAMS_NS = 'http://etherx.jabber.org/streams'
XMPP_VERSION = '1.0'
BOSH_VERSION = '1.6'
BOSH_CONTENT = 'text/xml; charset=utf-8'
XML_LANG = 'en'
BOSH_WAIT = 60
BOSH_HOLD = 1


class BOSHClient(object):
    def __init__(self, jid, password, bosh_service):
        """ Initialize the client.

        You must specify the Jabber ID, the corresponding password and the URL
        of the BOSH service to connect to.

        """
        self.log = logging.getLogger('conversejs.boshclient')
        self.log.addHandler(logging.NullHandler())

        self._connection = None
        self._sid = None
        
        self.jid, self.to = jid.split('@')
        self.password = password
        self.bosh_service = urlparse(bosh_service) 
        
        self.rid = randint(0, 10000000)
        self.log.debug('Init RID: %s' % self.rid)
        
        self.headers = {
            "Content-Type": "text/plain; charset=UTF-8",
            "Accept": "text/xml",
            "Accept-Encoding": "gzip, deflate"
        }
        
        self.server_auth = []
   
    @property 
    def connection(self):
        """Returns an stablished connection"""

        if self._connection:
            return self._connection

        self.log.debug('Initializing connection to %s' % (self.bosh_service.
                                                          netloc))
        if self.bosh_service.scheme == 'http':
            Connection = httplib.HTTPConnection
        elif self.bosh_service.scheme == 'https':
            Connection = httplib.HTTPSConnection
        else:
            # TODO: raise proper exception 
            raise Exception('Invalid URL scheme %s' % self.bosh_service.scheme)
        
        self._connection = Connection(self.bosh_service.netloc)
        self.log.debug('Connection initialized')
        # TODO add exceptions handler there (URL not found etc)

        return self._connection

    def close_connection(self):
        if not self._connection:
            self.log.debug('Trying to close connection before initializing it.')
            return 

        self.log.debug('Closing connection')
        self.connection.close()
        self.log.debug('Connection closed')
        # TODO add execptions handler there

    def get_body(self, sid_request=False):
        body = ET.Element('body')

        body.set('xmlns', HTTPBIND_NS)

        if sid_request:
            body.set('xmlns:xmpp', BOSH_NS) 
            body.set('wait', unicode(BOSH_WAIT))
            body.set('hold', unicode(BOSH_HOLD))
            body.set('content', BOSH_CONTENT)
            body.set('ver', unicode(BOSH_VERSION))

            body.set('xmpp:version', unicode(XMPP_VERSION))

            body.set('xml:lang', "en")

            body.set('to', self.to)

        if self._sid:
            body.set('sid', self.sid) 

        body.set('rid', str(self.rid))

        return body

    def send_request(self, xml_stanza):
        if isinstance(xml_stanza, ET.Element):
            xml_stanza = ET.tostring(xml_stanza, encoding='utf8', method='xml')

        self.log.debug('XML_STANZA: %s', xml_stanza)
        self.log.debug('Sending the request')

        self.connection.request("POST", self.bosh_service.path,
                                xml_stanza, self.headers)
        response = self.connection.getresponse()
        self.log.debug('Response status code: %s' % response.status)

        # Increment request id:
        #    http://xmpp.org/extensions/xep-0124.html#rids-syntax
        self.rid += 1

        if response.status == 200:
            data = response.read()
        else:
            self.log.debug('Something wrong happened!')
            return False

        self.log.debug('DATA: %s', data)
        return data

    @property
    def sid(self):
        if self._sid:
            return self._sid
        
        return self.request_sid()

    def request_sid(self):
        """ Request a BOSH session according to
        http://xmpp.org/extensions/xep-0124.html#session-request
        Returns the new SID (str).

        """
        if self._sid:
            return self._sid

        self.log.debug('Prepare to request BOSH session')
        
        data = self.send_request(self.get_body(sid_request=True))
        if not data:
            return None
      

        # This is XML. response_body contains the <body/> element of the
        # response.
        response_body = ET.fromstring(data)
        
        # Get the remote Session ID
        self._sid = response_body.get('sid')
        self.log.debug('sid = %s' % self._sid)
        
        # Get the longest time (s) that the XMPP server will wait before
        # responding to any request.
        self.server_wait = response_body.get('wait')
        self.log.debug('wait = %s' % self.server_wait)
        
        # Get the authid
        self.authid = response_body.get('authid')
        
        # Get the allowed authentication methods using xpath
        search_for = '{{{}}}features/{{{}}}mechanisms/{{{}}}mechanism'.format(
                                JABBER_STREAMS_NS, XMPP_SASL_NS, XMPP_SASL_NS)
        self.log.debug('Looking for "%s" into response body', search_for)
        mechanisms = response_body.iterfind(search_for)
        self.server_auth = []

        for mechanism in mechanisms:
            self.server_auth.append(mechanism.text) 
            self.log.debug('New AUTH method: %s' % mechanism.text)

        if not self.server_auth:
            self.log.debug(('The server didn\'t send the allowed '
                            'authentication methods'))
            self._sid = None
                    
        return self._sid

    def get_challenge(self, mechanism):
        body = self.get_body()
        auth = ET.SubElement(body, 'auth')
        auth.set('xmlns', XMPP_SASL_NS)
        auth.set('mechanism', mechanism)

        resp_root = ET.fromstring(self.send_request(body))
        challenge_node = resp_root.find('{{{}}}challenge'.format(XMPP_SASL_NS))

        if challenge_node is not None:
            return challenge_node.text 

        return None

    def send_challenge_response(self, response_plain):
        """Send a challenge response to server"""

        # Get a basic stanza body
        body = self.get_body()

        # Create a response tag and add the response content on it
        #   using base64 encoding
        response_node = ET.SubElement(body, 'response')  
        response_node.set('xmlns', XMPP_SASL_NS)
        response_node.text = base64.b64encode(response_plain)

        # Send the challenge response to server
        resp_root = ET.fromstring(self.send_request(body))

        # Look for the success tag. If it's not present authentication
        #   has failed 
        success = resp_root.find('{{{}}}success'.format(XMPP_SASL_NS))
        if success is not None:
            return True
        return False

    def authenticate_xmpp(self):
        """Authenticate the user to the XMPP server via the BOSH connection."""

        self.request_sid()

        self.log.debug('Prepare the XMPP authentication')

        # Instantiate a sasl object 
        sasl = SASLClient(host=self.to,
                         service='xmpp',
                         username=self.jid,
                         password=self.password)

        # Choose an auth mechanism
        sasl.choose_mechanism(self.server_auth, allow_anonymous=False)

        # Request challenge
        challenge = self.get_challenge(sasl.mechanism)
        
        # Process challenge and generate response
        response = sasl.process(base64.b64decode(challenge))

        # Send response
        success = self.send_challenge_response(response)
        if not success:
            return False

        self.request_restart()

        self.bind_resource()
        
        return True

    def bind_resource(self):
        body = self.get_body()

        iq = ET.SubElement(body, 'iq')
        iq.set('id', 'bind_1')
        iq.set('type', 'set')
        iq.set('xmlns', JABBER_CLIENT_NS) 

        bind = ET.SubElement(iq, 'bind')
        bind.set('xmlns', XMPP_BIND_NS)    

        self.send_request(body)

    def request_restart(self):
        body = self.get_body()
        body.set('xmpp:restart', 'true')
        body.set('xmlns:xmpp', BOSH_NS)
        self.send_request(body)

    def get_credentials(self):
        success = self.authenticate_xmpp()            
        if not success:
            return None, None, None

        return u'{}@{}'.format(self.jid, self.to), self.sid, self.rid 
        

if __name__ == '__main__':
    import sys

    if len(sys.argv) != 4:
        print 'usage: {} SERVICE_URL USERNAME PASSWORD'.format(sys.argv[0])
        sys.exit(1)

    c = BOSHClient(sys.argv[2], sys.argv[3], sys.argv[1])
    print c.get_credentials()
    c.close_connection()
