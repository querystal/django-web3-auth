=====
Usage
=====

To use Django-Web3-Auth in a project, add it to your `INSTALLED_APPS`:

.. code-block:: python

    INSTALLED_APPS = (
        ...
        'web3auth.apps.Web3AuthConfig',
        ...
    )

Add Django-Web3-Auth's URL patterns:

.. code-block:: python

    from web3auth import urls as web3auth_urls


    urlpatterns = [
        ...
        url(r'^', include(web3auth_urls)),
        ...
    ]
