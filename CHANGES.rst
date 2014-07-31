Changelog
=========

0.3.1 (2014-31-07)
------------

- Added support to Django 1.7 [@matheusfaria, @darksshades]
- Updated sleekxmpp version to 1.3.1


0.3 (2013-12-06)
------------

- Adding CONVERSEJS_ALLOW_CONTACT_REQUESTS configuration variable. [LuanP]
- Adding CONVERSEJS_SHOW_ONLY_ONLINE_USERS configuration variable. [LuanP]


0.2.9 (2013-11-26)
------------

- Adding timeout to BOSH connections [seocam]
- Adding function to change user password [LuanP]
- Moving/refactor registration functions to xmpp.py [LuanP]
- Better error handling on xmpp connections [LuanP]


0.2.8 (2013-10-20)
------------

- Python 2.6 compatibility fixes [chenhouwu]
- Allowing http responses to be gziped [chenhouwu]
- Fixing Digest-MD5 conformity issues [chenhouwu]
- Converse.js updated to 0.6.6 [seocam]


0.2.7 (2013-10-17)
------------

- Added CONVERSEJS_ENABLED setting. This allows the easily disable conversejs from the website. [seocam]
- Updating migration to make compatible with Django 1.5 Custom Users [seocam]
- Closing connections properly [seocam]


0.2.6 (2013-09-19)
------------------

- Added converse.js fonticons to static files [seocam]
- Converse.js updated. Version 0.6.4 still used but with a patch applied to CSS to avoid clashing with Bootstrap. [seocam]
- Updating setup to use pure-sasl from PyPI [seocam]


0.2.5 (2013-09-16)
------------------

- Fixed some python2.6 incompatibility issues [chenhouwu]
- Updated requirements on SleekXMPP [seocam]
- Updating converse.js from 0.6.3 to 0.6.4 [seocam]


0.2.4 (2013-09-12)
------------------

- Adding CONVERSEJS_AUTO_REGISTER option to automatically create a JID for a given django user [seocam]
- Updating converse.js from 0.6.2 to 0.6.3 [seocam]


0.2.3 (2013-08-31)
------------------

- Removed duplicated request asking for SASL DIGEST-MD5 challenge [seocam]
- Updating converse.js from 0.6.1 to 0.6.2 [seocam]


0.2.2 (2013-08-28)
------------------

- Updating converse.js from 0.5 to 0.6.1 [seocam]
- Using distribute instead of distutils [seocam]


0.2 (2013-08-26)
------------------

- Initial release [seocam]
