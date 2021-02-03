from django.urls import include,path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('dashboard', views.dashboard),
    path('', include('django.contrib.auth.urls')),
    path('', include('social_django.urls')),
    
]