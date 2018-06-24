import random
import string

from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.conf import settings
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse, HttpResponseBadRequest
from web3auth.forms import LoginForm, SignupForm
from web3auth.utils import recover_to_addr
from django.utils.translation import ugettext_lazy as _
from web3auth.settings import app_settings

import json
@require_http_methods(["GET", "POST"])
def login_api(request):
    if request.method == 'GET':
        token = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for i in range(32))
        request.session['login_token'] = token
        return JsonResponse({'data': token, 'success': True})
    else:
        token = request.session.get('login_token')
        if not token:
            return JsonResponse({'error': _(
                "No login token in session, please request token again by sending GET request to this url"),
                'success': False})
        else:
            form = LoginForm(token, request.POST)
            if form.is_valid():
                signature, address = form.cleaned_data.get("signature"), form.cleaned_data.get("address")
                del request.session['login_token']
                user = authenticate(request, token=token, address=address, signature=signature)
                if user:
                    login(request, user, 'web3auth.backend.Web3Backend')
                    redirect_url = request.GET.get('next') or request.POST.get('next') or settings.LOGIN_REDIRECT_URL
                    return JsonResponse({'success': True, 'redirect_url': redirect_url})
                else:
                    error = _("Can't find a user for the provided signature with address {address}").format(
                        address=address)
                    return JsonResponse({'success': False, 'error': error})
            else:
                return JsonResponse({'success': False, 'error': json.loads(form.errors.as_json())})

@require_http_methods(["POST"])
def signup_api(request):
    if not app_settings.WEB3AUTH_SIGNUP_ENABLED:
        return JsonResponse({'success': False, 'error': _("Sorry, signup's are currently disabled")})
    form = SignupForm(request.POST)
    if form.is_valid():
        user = form.save(commit=False)
        addr_field = app_settings.WEB3AUTH_USER_ADDRESS_FIELD
        setattr(user, addr_field, form.cleaned_data[addr_field])
        user.save()
        login(request, user, 'web3auth.backend.Web3Backend')
        redirect_url = request.GET.get('next') or request.POST.get('next') or settings.LOGIN_REDIRECT_URL
        return JsonResponse({'success': True, 'redirect_url': redirect_url})
    else:
        return JsonResponse({'success': False, 'error': json.loads(form.errors.as_json())})


def login_view(request, template_name='web3auth/login.html'):
    if request.method == 'POST':
        token = request.session['login_token']
        form = LoginForm(token, request.POST)
        if form.is_valid():
            if form.user is not None:
                del request.session['login_token']
                login(request, form.user)
                return redirect(request.GET.get('next') or request.POST.get('next') or settings.LOGIN_REDIRECT_URL)
            else:
                request.session['ethereum_address'] = recover_to_addr(token, form.cleaned_data['signature'])
                return redirect(signup_view)
    else:
        token = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(32))
        request.session['login_token'] = token
        form = LoginForm(token)
    return render(request,
                  template_name,
                  {'form': form,
                   'login_token': token})


def signup_view(request, template_name='web3auth/signup.html'):
    if request.method == 'POST':
        ethereum_address = request.session['ethereum_address']
        form = SignupForm(request.POST)
        if form.is_valid():
            del request.session['ethereum_address']
            user = form.save(commit=False)
            user.username = ethereum_address
            user.save()
            login(request, user)
            return redirect(request.GET.get('next') or request.POST.get('next') or settings.LOGIN_REDIRECT_URL)
    else:
        form = SignupForm()
    return render(request,
                  template_name,
                  {'form': form})
