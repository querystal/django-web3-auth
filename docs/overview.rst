========
Overview
========

Django-web3-auth features 1 view for login (with JSON responses)
and 2 views for Signup (one with JSON responses, and the other - using Django Forms and rendered templates).

It also has 2 forms, SignupForm (rendered) and LoginForm (uses hidden inputs, used to validate data only).

Possible configuration includes customizable address field (WEB3AUTH_USER_ADDRESS_FIELD), additional fields for User model (WEB3AUTH_USER_SIGNUP_FIELDS) and on/off switch for registration (WEB3AUTH_SIGNUP_ENABLED).
You can read more on that in the Configuration section.

The signup process is as follows (signup_view example, signup_api is similar):

1. User heads to the signup URL ({% url 'web3auth_signup' %})
2. The signup view is rendered with a SignupForm which includes WEB3AUTH_USER_SIGNUP_FIELDS and WEB3AUTH_USER_ADDRESS_FIELD
3. The user enters required data and clicks the submit button and the POST request fires to the same URL with signup_view
4. Signup view does the following:
    4.1. Creates an instance of a SignupForm.
    4.2. Checks if the registration is enabled.
    4.3. If the registration is closed or form has errors, returns form with errors
    4.4 If the form is valid, saves the user without saving to DB
    4.5. Sets the user address from the form, saves it to DB
    4.6. Logins the user using web3auth.backend.Web3Backend
    4.7. Redirects the user to LOGIN_REDIRECT_URL or 'next' in get or post params
5. The user is signed up and logged in

The login process is as follows (login_api example):

1. On some page of the website, there is Javascript which fires
2.




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
