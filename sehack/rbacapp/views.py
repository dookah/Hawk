from django.db.models import query
from django.shortcuts import render, redirect
from django.contrib.auth import logout as log_out
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.conf import settings as django_settings
from urllib.parse import urlencode
from .models import Integration
from django.core import serializers
import json
from api import views as api
import datetime
import traceback

def index(request):

    ctx = {
        'name' : 'Josh'
    }

    return render(request, 'index.html', ctx)

# Utility function for counting names / emails
def increment_or_append(list, string):
    for i in list:
        if(string == i[0]):
            i[1] = i[1] + 1
            return list
    list.append([string, 1])
    return list

# Utility function for detecting anomalies in names / emails
def find_anomalies(list):
    anomalies = []
    for i in list:
        if(i[1] == 1):
            anomalies.append(i[0])
    return anomalies

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

    query_set = Integration.objects.filter(user=userdata['user_id']).all()
    meraki_set = query_set.filter(product='meraki').all()
    ise_set = query_set.filter(product='ise').all()
    duo_set = query_set.filter(product='duo').all()
    viptela_set = query_set.filter(product='viptela').all()
    umbrella_set = query_set.filter(product='umbrella').all()
    webex_set = query_set.filter(product='webex').all()

    enabled = {
        'meraki': False,
        'ise': False,
        'duo': False,
        'viptela': False,
        'umbrella': False,
        'webex': False
    }

    names, emails = [], []

    meraki, ise, duo, viptela, umbrella, webex = "", "", "", "", "", ""
    try:
        if(list(meraki_set.values())[0]['enabled'] == True):
            try:
                meraki = api.meraki(request)
                for i in meraki:
                    if i['lastActive'] is not "":
                        i['lastActive'] = datetime.datetime.fromtimestamp(i['lastActive'])
                    names = increment_or_append(names, i['name'])
                    emails = increment_or_append(emails, i['email'])
                enabled['meraki'] = True
            except:
                meraki = ""
                enabled['meraki'] = 'error'
                print("Meraki API failed")
    except:
        print("error")

    try:
        if(list(ise_set.values())[0]['enabled'] == True):
            try:
                ise = api.ise(request)
                for i in ise:
                    names = increment_or_append(names, i['name'])
                enabled['ise'] = True
            except:
                ise = ""
                enabled['ise'] = 'error'
                print("ISE API failed")
    except:
        print("error")

    try:
        if(list(duo_set.values())[0]['enabled'] == True):
            try:
                duo = api.duo(request)
                enabled['duo'] = True
            except:
                duo = ""
                enabled['duo'] = 'error'
                print("Duo API failed")
    except:
        print("error")

    try:
        if(list(umbrella_set.values())[0]['enabled'] == True):
            try:
                umbrella = api.umbrella(request)
                for i in umbrella:
                    str_time = i['lastLoginTime']
                    d = datetime.datetime.strptime(str_time, "%Y-%m-%dT%H:%M:%S.%fZ")
                    i['lastLoginTime'] = d
                    fullname = str(i['firstname']) + ' ' + str(i['lastname'])
                    names = increment_or_append(names, fullname)
                    emails = increment_or_append(emails, i['email'])
                enabled['umbrella'] = True
            except:
                umbrella = ""
                enabled['umbrella'] = 'error'
                print("Umbrella API failed")
    except:
        print("error")

    names_anomalies = find_anomalies(names)
    emails_anomalies = find_anomalies(emails)

    # If only one product is configured, there should be no anomalies
    enabled_count = 0
    for product in enabled:
        if(enabled[product] == True):
            enabled_count = enabled_count + 1
    if(enabled_count == 1):
        names_anomalies = []
        emails_anomalies = []

    try:
        # Get ISE host for dashboard link
        ise_host = ise_set.values()[0]['host']
    except:
        print("error")
    

    return render(request, 'dashboard.html', {
        'auth0User': auth0user,
        'userdata': json.dumps(userdata, indent=4),
        'enabled': enabled,
        'meraki': meraki,
        'ise': ise,
        'duo': duo,
        'umbrella': umbrella,
        'names_anomalies': names_anomalies,
        'emails_anomalies': emails_anomalies,
        'ise_host': ise_host
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
                 (django_settings.SOCIAL_AUTH_AUTH0_DOMAIN, django_settings.SOCIAL_AUTH_AUTH0_KEY, return_to)
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

    query_set = Integration.objects.filter(user=userdata['user_id']).all()
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