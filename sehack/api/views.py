from django.db.models import query
from django.shortcuts import render, redirect
from django.contrib.auth import logout as log_out
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.conf import settings
from urllib.parse import urlencode
from django.core import serializers
from requests.api import head
from rbacapp.models import Integration
import requests
import json
import sys, duo_client

# Create your views here.
def index(request):
    return HttpResponse("Hello, world. You're at the api index.")

@login_required
def meraki(request):
    #Retrieve the user ID from the authenticated auth0 session
    user = request.user
    auth0user = user.social_auth.get(provider='auth0')
    user_id = auth0user.uid;

    query_set = Integration.objects.filter(user=user_id).all()
    meraki_set = query_set.filter(product='meraki').all()

    parameters = meraki_set.values()[0]

    


    host = 'https://api.meraki.com/api/v0/organizations'

    headers = {
        'X-Cisco-Meraki-API-Key' : parameters['ikey']
    }
    
    request = requests.get(host, headers=headers)

    

    org_id = request.json()[0]['id']

    path = '/' + org_id + '/admins'
    request = requests.get(host + path, headers=headers)

    

    return request.json()

@login_required
def ise(request):
    #Retrieve the user ID from the authenticated auth0 session
    user = request.user
    auth0user = user.social_auth.get(provider='auth0')
    user_id = auth0user.uid;

    query_set = Integration.objects.filter(user=user_id).all()
    ise_set = query_set.filter(product='ise').all()

    parameters = ise_set.values()[0]

    host = 'https://' + parameters['host'] + ':9060/ers/config/adminuser'

    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }

    request = requests.get(host, auth=(parameters['username'], parameters['password']), headers=headers, verify=False)

    return request.json()

@login_required
def duo(request):
    #Retrieve the user ID from the authenticated auth0 session
    user = request.user
    auth0user = user.social_auth.get(provider='auth0')
    user_id = auth0user.uid;

    query_set = Integration.objects.filter(user=user_id).all()
    duo_set = query_set.filter(product='duo').all()

    parameters = duo_set.values()[0]

    admin_api = duo_client.Admin(
        ikey=parameters['ikey'],
        skey=parameters['skey'],
        host=parameters['host']
    )

    output = admin_api.get_admins()

    return output

@login_required
def umbrella(request):
    #Retrieve the user ID from the authenticated auth0 session
    user = request.user
    auth0user = user.social_auth.get(provider='auth0')
    user_id = auth0user.uid;

    query_set = Integration.objects.filter(user=user_id).all()
    umbrella_set = query_set.filter(product='umbrella').all()

    parameters = umbrella_set.values()[0]

    org = parameters['host']
    ikey = parameters['ikey']
    skey = parameters['skey']

    host = 'https://management.api.umbrella.com/v1/organizations/' + org + '/users'

    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    
    response = requests.get(host, auth=requests.models.HTTPBasicAuth(ikey, skey), headers=headers)

    users = json.loads(response.text)
    admins = []
    for user in users:
        if(user['role'] == 'Full Admin'):
            admins.append(user)

    return admins

@login_required
def viptela(request):
    #Retrieve the user ID from the authenticated auth0 session
    user = request.user
    auth0user = user.social_auth.get(provider='auth0')
    user_id = auth0user.uid

    query_set = Integration.objects.filter(user=user_id).all()
    viptela_set = query_set.filter(product='viptela').all()

    parameters = viptela_set.values()[0]

    host = parameters['host']
    username = parameters['username']
    password = parameters['password']
    root = 'https://' + host

    #Get a security token from vManage
    auth_url = root + '/j_security_check'
    auth_payload = 'j_username=' + username + '&j_password=' + password
    auth_header = {
        'Content-Type' : 'application/x-www-form-urlencoded'
    }
    auth_response = requests.request("POST", auth_url, headers=auth_header, data = auth_payload)

    cookie = auth_response.cookies.items()[0][0] + '=' + auth_response.cookies.items()[0][1]

    cookie_header = {
        'Cookie' : cookie
    }

    CSRF_url = root + '/dataservice/client/token'
    
    token_response = requests.request("GET", CSRF_url, headers=cookie_header, data=auth_payload)
    token = token_response.text

    url = root + ':443/dataservice/admin/user'
    headers = {
        'X-XSRF-TOKEN': token,
        'Cookie': cookie
    }

    response = requests.request("GET", url, headers=headers)

    return response.json()['data']


@login_required
def insert_integrations(request):
    integrations = json.loads(request.body)
    for parameters in integrations:
        obj, created = Integration.objects.select_for_update().update_or_create(
            user = parameters['user'], product = parameters['product'],
            defaults = {
                'host': parameters['host'],
                'ikey': parameters['ikey'],
                'skey': parameters['skey'],
                'username': parameters['username'],
                'password': parameters['password'],
                'enabled': parameters['enabled']
            }
        )
    
    return HttpResponse("")
