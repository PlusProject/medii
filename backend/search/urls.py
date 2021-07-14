from django.urls import path
from django.urls.resolvers import URLPattern
from . import views

urlpatterns = [
    path('', views.DoctorTest.as_view(), name='DoctorTest'),
    path('name', views.SearchName.as_view(), name='SearchName'),
    path('hospital', views.SearchHospital.as_view(), name='SearchHospital'),
]