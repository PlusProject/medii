from rest_framework import response
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from .models import ClinicalTrials, Disease, Person, Participate, Writes, Thesis
from .serializers import (ClinicalTrialsSerializer, HospitalSerializer, ThesisSerializer, NameSerializer, 
                            PersonSerializer, ParticipateSerializer, WritesSerializer, 
                            CrisCoworkerSerializer, ThesisCoworkerSerializer, DiseaseSerializer)
from django.db.models import Q
import re

class SearchAPI(APIView):
    def get(self, request):
        name = request.GET.get('doctor_name')
        hospital = request.GET.get('hospital')
        major = request.GET.get('major')
        disease = request.GET.get('disease')
        rare = request.GET.get('rare')

        personQuery = Person.objects.all()

        if name:
            personQuery = personQuery.filter(name_kor__icontains=name)
        
        if hospital:
            personQuery = personQuery.filter(belong__contains=hospital)

        if major:
            personQuery = personQuery.filter(major__contains=major)

        pid_list = [person.pid for person in personQuery]

        if disease:
            if re.compile('[a-zA-Z]\d{2}').search(disease):
                clinicalTrialsQuery = ClinicalTrials.objects.filter(disease_code__icontains=disease)
            else:
                clinicalTrialsQuery = ClinicalTrials.objects.filter(disease_detail__contains=disease)

            if rare=='true':
                clinicalTrialsQuery = clinicalTrialsQuery.filter(rare_disease=True)
            cid_list = [trial.cid for trial in clinicalTrialsQuery]
            pid_in_participate = []

            for cid in cid_list:
                tempQuery = Participate.objects.filter(cid=cid)
                participate_list = [p.pid.pid for p in tempQuery]
                pid_in_participate += participate_list

            pid_list = sorted((set(pid_list).intersection(pid_in_participate)))

        if re.compile('[a-zA-Z]\d{2}').search(disease):
            rare_disease = Disease.objects.filter(code=disease).values('rare')
        elif re.compile('[가-힣]+').search(disease):
            rare_disease = Disease.objects.filter(name_kor=disease).values('rare')
        else:
            rare_disease = Disease.objects.filter(name_eng=disease).values('rare')

        person = PersonSerializer(Person.objects.filter(pid__in=pid_list), many=True)
        return Response({
            'person': person.data,
            'rare': True if rare_disease else False
        })


class SearchClinicalTrialsAPI(APIView):
    def get(self, request):
        disease = request.GET.get('disease')
        rare = request.GET.get('rare')

        if re.compile('[a-zA-Z]\d{2}').search(disease):
            clinicalTrialsQuery = ClinicalTrials.objects.filter(disease_code__icontains=disease)
        else:
            clinicalTrialsQuery = ClinicalTrials.objects.filter(disease_detail__contains=disease)

        if rare=='true':
            clinicalTrialsQuery = clinicalTrialsQuery.filter(rare_disease=True)
        return Response(ClinicalTrialsSerializer(clinicalTrialsQuery, many=True).data)


class ClinicalTrialsAPI(APIView):
    def get(self, request):
        pid = request.GET.get('pid')
        keyword = request.GET.get('keyword')
        participateQuery = Participate.objects.filter(pid=pid)
        participate = ParticipateSerializer(participateQuery, context={"keyword": keyword}, many=True)
        
        return Response(participate.data)
        # return Response({
        #     'participate': participate.data,
        #     # 'filtered_cid': 
        # })


class ThesisAPI(APIView):
    def get(self, request):
        pid = request.GET.get('pid')
        writesQuery = Writes.objects.filter(pid=pid)
        writes = WritesSerializer(writesQuery, many=True)
        return Response(writes.data)


@api_view(['GET'])
def name_list(request):
    nameQuery = Person.objects.filter(job='의사').values('name_kor')
    name = NameSerializer(nameQuery, many=True)
    return Response(name.data)


@api_view(['GET'])
def hospital_list(request):
    hospitalQuery = Person.objects.filter(job='의사').values('belong').distinct()
    hospital = HospitalSerializer(hospitalQuery, many=True)
    return Response(hospital.data)


@api_view(['GET'])
def disease_list(request):
    diseases = Disease.objects.all()
    return Response(DiseaseSerializer(diseases, many=True).data)


@api_view(['GET'])
def rare_disease_list(request):
    diseases = Disease.objects.filter(rare=True)
    return Response(DiseaseSerializer(diseases, many=True).data)


@api_view(['GET'])
def get_coworker(request):
    pid = request.GET.get('pid')
    writes = Writes.objects.filter(pid=pid)
    tid_list = [thesis.tid.tid for thesis in writes]

    # coworker_list = []
    # for tid in tid_list:
    #     thesis_title = Thesis.objects.get(tid=tid).title
    #     coworker = Thesis.objects.filter(title=thesis_title)
    #     if len(coworker) > 1:
    #         coworker_list += coworker[1:]
    # print(coworker_list)
    # return Response(ThesisSerializer(coworker_list, many=True).data)
    coworker_list = []
    for tid in tid_list:
        thesis = Thesis.objects.get(tid=tid)
        thesis_title = thesis.title
        thesis_tid = thesis.tid
        coworker = Thesis.objects.filter(title=thesis_title).exclude(tid=thesis_tid)
        if len(coworker) > 0:
            coworker_list += coworker
    return Response(ThesisCoworkerSerializer(coworker_list, many=True).data)

# @api_view(['GET'])
class CrisCoworkerAPI(APIView):
    def get(self, request):
        pid = request.GET.get('pid')
        participate = Participate.objects.filter(pid=pid, source_name="CRIS")
        cid_list = [[cris.cid.cid, cris.position] for cris in participate]

        coworker_list = []
        for cid, position in cid_list:
            participate_list = Participate.objects.filter(cid=cid).exclude(position=position)
            if len(participate_list) >= 1:
                coworker_list += participate_list
        return Response(CrisCoworkerSerializer(coworker_list, many=True).data)