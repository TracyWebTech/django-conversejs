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

.. code-block::

    pip install git+https://github.com/TracyWebTech/pure-sasl@digestmd5

Install django-conversejs:

.. code-block::

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

.. code-block::

    python manage.py syncdb
    python manage.py migrate # optinal
    
    
Converse.js Version
-------------------

We currently ship Converse.js **v0.5**.

If you need a newer version, please open an issue or a pull request.
