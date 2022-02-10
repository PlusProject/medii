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
    path('recommend', views.RecommendAPI.as_view(), name='Recommend'),
    path('recommend2', views.Recommend2API.as_view(), name='Recommend2'),
    path('count', views.CountAPI.as_view(), name='Count'),
    path('diseasematch', views.DiseaseMatchAPI.as_view(), name='DiseaseMatch'),
    path('extractdisease', views.ExtractDieaseAPI.as_view(), name='ExtractDisease'),
    path('socialnetwork', views.snpaper_view, name="snpaper_view"),
    path('socialnetwork_cnt', views.snpapercnt_view, name="snpapercnt_view"),
    path('socialnetwork_cris', views.nodecris_view, name="nodecris_view"),
    path('socialnetwork_cris_cnt', views.nodecriscnt_view, name="nodecriscnt_view"),
    path('snpaperedgeyear', views.snpaperedgeyear_view, name="snpaperedgeyear_view"),
    path('nodes', views.nodes_view, name="nodes_view"),
    path('crisedge', views.crisedge_view, name="crisedge_view"),
    # path('coworker_cris', views.get_cris_coworker, name="CrisCoworker"),
]