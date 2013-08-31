django-conversejs
=================

This app aims to make easier to integrate `Converse.js`_ into Django.

Currently ``django-conversejs`` provides:

* A minified distribution of converse.js
* Template tags to help you to include converse.js on your Django project
* A database model to store the XMPP user and password for each user
* Converse.js configurations through settings.py
* Single-sign-on (SSO) like experience


.. _Converse.js: http://conversejs.org/


Installing and configuring
---------------------------

Install pure-sasl from ``TracyWebTech/digestmd5`` branch:

::

    pip install git+https://github.com/TracyWebTech/pure-sasl@digestmd5

Install django-conversejs:

::

    pip install git+https://github.com/TracyWebTech/django-conversejs

Add ``conversejs`` to installed apps in your settings.py:

.. code-block:: python

    INSTALLED_APPS = {
        ...
        'conversejs',
        ...
    }

Configure the BOSH service URL in your settings.py:

.. code-block:: python
    
    CONVERSEJS_BOSH_SERVICE_URL = 'https://my-bosh-service.com'

Load the static files in your templates using django-conversejs custom tags:

.. code-block:: html+django

    {% load conversejs %}
    ...
    <head>
      ...
      {% conversejs_static %}
      ...
    </head>

Load the chat panel and the Javascript initilizalizer also using our custom tags:

.. code-block:: html+django

    {% load conversejs %}
    ...
    
      {% conversejs_chatpanel %}
      {% conversejs_initialize %}
    </body>

Update database schema:

::

    python manage.py syncdb
    python manage.py migrate # optional


Adding an XMPP account
----------------------

* Log in the Django Admin

* Add an XMPP account by clicking in the '+ Add' button

* Choose the user from the select box and them type the JabberID and password for the account

Now everytime the select user your logs in your site he will be automaticaly logged in the XMPP
server using the credentials you provided.


Forms
------

If you want to create custom forms to keep the look and feel of your site you can use
conversejs.forms as a start point.


Converse.js Version
-------------------

We currently ship Converse.js **v0.6.2**.

If you need a newer version, please open an issue or a pull request.



IMPORTANT NOTE:
---------------

django-conversejs depends of `pure-sasl`, a Python library to perform SASL authentication.

Currently the stable version of pure-sasl has a bug which doesn't allow us to use
DIGEST-MD5 authentication, which happens to be the most recommend authentication
method. That's why this instructions ask you to install pure-sasl from a repository
which is not the official one. As soon as `pure-sasl` authors get the bugs fixed 
we'll update the instructions.

Sorry for the inconvenience.
