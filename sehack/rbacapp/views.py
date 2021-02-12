from django.db.models import query
from django.shortcuts import render, redirect
from django.contrib.auth import logout as log_out
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.conf import settings
from urllib.parse import urlencode
from .models import Integration
from django.core import serializers
import json

def index(request):

    ctx = {
        'name' : 'Josh'
    }

    return render(request, 'index.html', ctx)
    
# Create your views here.


@login_required
def dashboard(request):
    user = request.user
    auth0user = user.social_auth.get(provider='auth0')
    userdata = {
        'user_id': auth0user.uid,
        'name': user.first_name,
        'picture': auth0user.extra_data['picture'],
        'email': auth0user.extra_data['email'],
    }

    return render(request, 'dashboard.html', {
        'auth0User': auth0user,
        'userdata': json.dumps(userdata, indent=4)
    })

@login_required
def profile(request):
    user = request.user
    auth0user = user.social_auth.get(provider='auth0')
    userdata = {
        'user_id': auth0user.uid,
        'name': user.first_name,
        'picture': auth0user.extra_data['picture'],
        'email': auth0user.extra_data['email'],
    }

    return render(request, 'profile.html', {
        'auth0User': auth0user,
        'userdata': json.dumps(userdata, indent=4)
    })

def logout(request):
    log_out(request)
    return_to = urlencode({'returnTo': request.build_absolute_uri('/')})
    logout_url = 'https://%s/v2/logout?client_id=%s&%s' % \
                 (settings.SOCIAL_AUTH_AUTH0_DOMAIN, settings.SOCIAL_AUTH_AUTH0_KEY, return_to)
    return HttpResponseRedirect(logout_url)

def settings(request):
    user = request.user
    auth0user = user.social_auth.get(provider='auth0')#
    userdata = {
        'user_id': auth0user.uid,
        'name': user.first_name,
        'picture': auth0user.extra_data['picture'],
        'email': auth0user.extra_data['email'],
    }

    query_set = Integration.objects.all()
    meraki_set = query_set.filter(product='meraki').all()
    ise_set = query_set.filter(product='ise').all()
    duo_set = query_set.filter(product='duo').all()
    viptela_set = query_set.filter(product='viptela').all()
    umbrella_set = query_set.filter(product='umbrella').all()
    webex_set = query_set.filter(product='webex').all()

    return render(request, 'settings.html', {
        'auth0User': auth0user,
        'userdata': json.dumps(userdata, indent=4),
        'integrations': list(query_set.values()),
        'meraki': list(meraki_set.values()),
        'ise': list(ise_set.values()),
        'duo': list(duo_set.values()),
        'viptela': list(viptela_set.values()),
        'umbrella': list(umbrella_set.values()),
        'webex': list(webex_set.values()),
    })