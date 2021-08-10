from django.urls import path
from django.urls.resolvers import URLPattern
from . import views

urlpatterns = [
    path('', views.SearchAPI.as_view(), name='Search'),
    path('searchClinicalTrials', views.SearchClinicalTrialsAPI.as_view(), name='SearchClinical'),
    path('clinicaltrials', views.ClinicalTrialsAPI.as_view(), name='ClinicalTrials'),
    path('thesis', views.ThesisAPI.as_view(), name='Thesis'),
    path('name', views.name_list, name="Name"),
    path('hospital', views.hospital_list, name="Hospital"),
    path('coworker', views.get_coworker, name="Coworker"),
    path('coworker_cris', views.CrisCoworkerAPI.as_view(), name="CrisCoworker"),
    path('disease', views.disease_list, name="disease_list"),
    path('rare_disease', views.rare_disease_list, name="rare_disease_list"),
    # path('coworker_cris', views.get_cris_coworker, name="CrisCoworker"),
]