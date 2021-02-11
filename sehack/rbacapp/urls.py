from django.urls import include,path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('dashboard', views.dashboard),
    path('profile', views.profile),
    path('logout', views.logout),
    path('', include('django.contrib.auth.urls')),
    path('', include('social_django.urls')),
    path('settings', views.settings)
    
]