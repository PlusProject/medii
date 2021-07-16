from django.urls import path
from django.urls.resolvers import URLPattern
from . import views

urlpatterns = [
    path('', views.SearchAPI.as_view(), name='Search'),
    path('clinicaltrials', views.ClinicalTrialsAPI.as_view(), name='ClinicalTrials'),
    path('thesis', views.ThesisAPI.as_view(), name='Thesis'),
    # path('hospital', views.SearchHospital.as_view(), name='SearchHospital'),
]