from django.db import models
from rest_framework import serializers
from .models import ClinicalTrials, Doctor, Person, Participate, Thesis, Writes

class DoctorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Doctor
        fields = ['major', 'education', 'career', 'url']


class PersonSerializer(serializers.ModelSerializer):
    #doctor_info = DoctorSerializer(source='pid', read_only=True)

    class Meta:
        model = Person
        fields = '__all__'


class ClinicalTrialsSerializer(serializers.ModelSerializer):

    class Meta:
        model = ClinicalTrials
        fields = '__all__'


class ThesisSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Thesis
        fields = ['tid', 'title', 'journal', 'year', 'citation', 'coworker']


class ParticipateSerializer(serializers.ModelSerializer):
    clinical_trials = ClinicalTrialsSerializer(source='cid', read_only=True)

    class Meta:
        model = Participate
        fields = ['clinical_trials', 'position', 'source_name']


class WritesSerializer(serializers.ModelSerializer):
    thesis = ThesisSerializer(source='tid', read_only=True)

    class Meta:
        model = Writes
        fields = ['thesis']
