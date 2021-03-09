# Cisco Q3 SE Hack - Hawk
### Correlate administrators across the Cisco product portfolio to detect anomalies and changes to role-based access control.

## What
Hawk is a Django based SaaS security tool, which displays administrators in the Cisco Portfolio. Monitoring Administators typically has been a manual task, which is prone to human error and miscommunication. The goal is to simplify this for SecOps teams, enabling them to monitor who has R/W access. 

## Assumptions
1. Python 3 is installed.
2. Have an Auth0 account for SSO. 
3. DUO 2FA is recommended. 
4. API Access to any products you'd like to integrate. 

## Deploy
### Step One
Hawk has a number of dependencies, you can install these from the requirements.txt file.
```Python
(./) pip install -r requirements.txt
```
### Step Two
Hawk makes use of a number of enviroment variables, you'll need to populate these in your deployment enviroment. 
```Python
django_key = RANDOM_STRING_HERE
```
```Python
django_key = RANDOM_STRING_HERE
```
```Python
auth0_domain = DOMAIN FROM AUTH0
```
```Python
auth0_key = KEY FROM AUTH0
```
```Python
auth0_secret = SECRET FROM AUTH0
```
### Step Three
Hawk makes use of a SQLite server for API key retention, you will need to execute a Django Migration for this to function correctly.
```Python
python manage.py migrate
```
### Step Four
You can use the in-built Django Web-Server, however it is recommended to use a production ready web-server.
```Python
python manage.py runserver 3000
```

### Step Five
Auth0 has a number of steps to validate authetnication requests, you will need to upload the domain you are running the server from to your auth0 Dashboard, you can find out more about this [here](https://auth0.com/docs/quickstart/webapp/django/01-login).

## Other
### Supported Products
We currently support as small subset of Cisco Security Products, you can find these below.
1. Meraki Dashboard
2. Identity Services Engine
3. Cisco SD-WAN (Formerly Viptela) 
4. Umbrella
5. Duo (Roadmap)
6. WebEx (Roadmap)
