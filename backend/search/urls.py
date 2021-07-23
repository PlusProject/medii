from django.urls import path
from django.urls.resolvers import URLPattern
from . import views

urlpatterns = [
    path('', views.SearchAPI.as_view(), name='Search'),
    path('clinicaltrials', views.ClinicalTrialsAPI.as_view(), name='ClinicalTrials'),
    path('thesis', views.ThesisAPI.as_view(), name='Thesis'),
    path('name', views.name_list, name="Name"),
    path('hospital', views.hospital_list, name="Hospital"),
    # path('hospital', views.SearchHospital.as_view(), name='SearchHospital'),
]