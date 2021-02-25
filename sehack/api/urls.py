from django.urls import include,path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('meraki', views.meraki, name='meraki'),
    path('viptela', views.viptela, name='viptela'),
    path('insert_integrations', views.insert_integrations)
]