"""jBeam URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from beam import requests as beam_requests

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('beam.urls')),

    path('post/ajax/validate/update_point_load', beam_requests.update_point_load, name = "update_point_load"),
    path('get/ajax/validate/get_diagrams', beam_requests.get_diagrams, name = "get_diagrams"),
]
