from django.db import models
from rest_framework import serializers
from .models import ClinicalTrials, Doctor, Person, Participate, Thesis, Writes

class DoctorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Doctor
        fields = '__all__'

class PersonSerializer(serializers.ModelSerializer):
    doctor_info = DoctorSerializer(source='doctor', read_only=True)
    # participate_test = serializers.StringRelatedField(many=True, read_only=True)
    # writes_test = serializers.StringRelatedField(many=True, read_only=True)
    participate_num = serializers.SerializerMethodField(read_only=True)
    writes_num = serializers.SerializerMethodField(read_only=True)
    
    def get_participate_num(self, instance):
        return instance.participate.count()

    def get_writes_num(self, instance):
        return instance.writes.count()

    class Meta:
        model = Person
        fields = '__all__'


class NameSerializer(serializers.ModelSerializer):

    class Meta:
        model = Person
        fields = ['name_kor']


class HospitalSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Person
        fields = ['belong']


class ClinicalTrialsSerializer(serializers.ModelSerializer):

    class Meta:
        model = ClinicalTrials
        fields = '__all__'


class ThesisSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Thesis
        fields = ['tid', 'title', 'journal', 'publication_date', 'citation', 'coworker']


class ParticipateSerializer(serializers.ModelSerializer):
    # person = PersonSerializer(source='pid', read_only=True)
    clinical_trials = ClinicalTrialsSerializer(source='cid', read_only=True)

    class Meta:
        model = Participate
        fields = '__all__'


class WritesSerializer(serializers.ModelSerializer):
    # person = PersonSerializer(source='pid', read_only=True)
    thesis = ThesisSerializer(source='tid', read_only=True)

    class Meta:
        model = Writes
        fields = ['pid', 'thesis']
