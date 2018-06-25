=============================
Django-Web3-Auth
=============================

.. image:: https://badge.fury.io/py/django-web3-auth.svg
    :target: https://badge.fury.io/py/django-web3-auth

.. image:: https://travis-ci.org/Bearle/django-web3-auth.svg?branch=master
    :target: https://travis-ci.org/Bearle/django-web3-auth

.. image:: https://codecov.io/gh/Bearle/django-web3-auth/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/Bearle/django-web3-auth

django-web3-auth is a pluggable Django app that enables login/signup via an Ethereum wallet (a la CryptoKitties). The user authenticates themselves by digitally signing the session key with their wallet's private key.

Documentation
-------------

The full documentation is at https://django-web3-auth.readthedocs.io.

Quickstart
----------
django-web3-auth has no releases yet, you'll need to install it from repository::

    pip install https://github.com/Bearle/django-web3-auth/archive/master.zip

When it becomes available on pypi, install Django-Web3-Auth with pip::

    pip install django-web3-auth

Add it to your `INSTALLED_APPS`:

.. code-block:: python

    INSTALLED_APPS = (
        ...
        'web3auth.apps.Web3AuthConfig',
        ...
    )
Set `'web3auth.backend.Web3Backend'` as your authentication backend:
.. code-block:: python

    AUTHENTICATION_BACKENDS = ['web3auth.backend.Web3Backend']

Add Django-Web3-Auth's URL patterns:

.. code-block:: python

    from web3auth import urls as web3auth_urls


    urlpatterns = [
        ...
        url(r'^', include(web3auth_urls)),
        ...
    ]

Features
--------

* TODO

Things to cover in docs
-----------------------
1. Installation
2. Overview of the login/signup process
3. Quickstart
4. Configuration
5. API signup/login
6. Forms & views, normal signup login
7. Usage with allauth, allauth-2fa
8. Supported web3 providers
9. Example project

- how to deal with passwords (which are not set during signup)
- why do user has to sign a message (opposed to myetherwallet & other dapps)
- address_field MUST be unique (otherwise the user can login as another user)



Running Tests
-------------

Does the code actually work?

::

    source <YOURVIRTUALENV>/bin/activate
    (myenv) $ pip install tox
    (myenv) $ tox

Credits
-------

Tools used in rendering this package:

*  Cookiecutter_
*  `cookiecutter-djangopackage`_

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`cookiecutter-djangopackage`: https://github.com/pydanny/cookiecutter-djangopackage
