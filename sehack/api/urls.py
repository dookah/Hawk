from django.urls import include,path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('meraki', views.meraki, name='meraki')
]