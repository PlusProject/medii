from django.db import models
from rest_framework import serializers
from rest_framework.fields import SerializerMethodField
from .models import ClinicalTrials, Disease, Doctor, Person, Participate,Thesis, DoctorAll, DoctorAll2, Writes, Totaldisease, DoctorTotalDisease, DoctorAllscore, SnPaper, SnPaperCnt, NodeCris,NodeCrisCnt,SnPaperEdgeYear, Nodes,CrisEdge


class SnPaperEdgeYearSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = SnPaperEdgeYear
        fields = "__all__"

class NodesSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Nodes
        fields = "__all__"

class CrisEdgeSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = CrisEdge
        fields = "__all__"
        
class DoctorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Doctor
        fields = "__all__"


class PersonSerializer(serializers.ModelSerializer):
    doctor_info = DoctorSerializer(source="doctor", read_only=True)
    participate_num = serializers.SerializerMethodField(read_only=True)
    writes_num = serializers.SerializerMethodField(read_only=True)

    def get_participate_num(self, instance):
        return instance.participate.count()

    def get_writes_num(self, instance):
        return instance.writes.count()

    class Meta:
        model = Person
        fields = "__all__"


class NameSerializer(serializers.ModelSerializer):

    class Meta:
        model = Person
        fields = ("name_kor",)


class HospitalSerializer(serializers.ModelSerializer):

    class Meta:
        model = Person
        fields = ("belong",)


class ClinicalTrialsSerializer(serializers.ModelSerializer):

    class Meta:
        model = ClinicalTrials
        fields = "__all__"


class ThesisSerializer(serializers.ModelSerializer):

    class Meta:
        model = Thesis
        fields = ("tid", "title", "journal",
                  "publication_date", "citation", "coworker",)


class ParticipateSerializer(serializers.ModelSerializer):
    # person = PersonSerializer(source="pid", read_only=True)
    clinical_trials = ClinicalTrialsSerializer(source="cid", read_only=True)
    # filtered_cid = serializers.SerializerMethodField()

    # def get_filtered_cid(self, obj):
    #     keyword = self.context["keyword"]
    #     if keyword:

    #     else:
    #         return 0

    class Meta:
        model = Participate
        fields = "__all__"


class WritesSerializer(serializers.ModelSerializer):
    # person = PersonSerializer(source="pid", read_only=True)
    thesis = ThesisSerializer(source="tid", read_only=True)

    class Meta:
        model = Writes
        fields = ("pid", "thesis",)


class ThesisCoworkerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Thesis
        fields = ("tid", "title",)


class CrisCoworkerSerializer(serializers.ModelSerializer):
    person = PersonSerializer(source="pid", read_only=True)

    class Meta:
        model = Participate
        fields = ("person", "cid", "position",)


class DiseaseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Disease
        fields = "__all__"


class DoctorTotalDiseaseSerializer(serializers.ModelSerializer):

    class Meta:
        model = DoctorTotalDisease
        fields = "__all__"


class TotalDiseaseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Totaldisease
        fields = "__all__"


class DoctorAllscoreSerializer(serializers.ModelSerializer):

    class Meta:
        model = DoctorAllscore
        fields = "__all__"

#동완
class SnPaperSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = SnPaper
        fields = "__all__"


class SnPaperCntSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = SnPaperCnt
        fields = "__all__"

class NodeCrisSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = NodeCris
        fields = "__all__"


class NodeCrisCntSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = NodeCrisCnt
        fields = "__all__"


        


class DoctorAllSerializer(serializers.ModelSerializer):

    class Meta:
        model = DoctorAll
        fields = "__all__"



class DoctorAll2Serializer(serializers.ModelSerializer):

    class Meta:
        model = DoctorAll2
        fields = "__all__"


class DoctorAll3Serializer(serializers.ModelSerializer):

    class Meta:
        model = DoctorAll2
        fields = "__all__"
