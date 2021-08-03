from django.shortcuts import render
from rest_framework import viewsets
from rest_framework import response
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from .models import ClinicalTrials, Doctor, Person, Participate, Writes, Thesis
from .serializers import HospitalSerializer, ThesisSerializer, NameSerializer, PersonSerializer, ParticipateSerializer, WritesSerializer
from itertools import chain
from django.db.models import Q
# Create your views here.

class SearchAPI(APIView):
    def get(self, request):
        name = request.GET.get('doctor_name')
        hospital = request.GET.get('hospital')
        major = request.GET.get('major')
        disease = request.GET.get('disease')
        personQuery = Person.objects.filter(name_kor__contains=name, belong__contains=hospital, major__contains=major)
        pid_list = [person.pid for person in personQuery]
        # 연결된 cid 뽑기...실패.......ㅠ
        # if disease:
        #     clinicalTrialsQuery = ClinicalTrials.objects.filter(disease_detail__contains=disease)
        #     cid_dict = { trial.cid: [] for trial in clinicalTrialsQuery }
        #     cid_not_in_participate = []

        #     for cid, pid in cid_dict.items():
        #         participateSet = Participate.objects.filter(cid=cid)
        #         if participateSet:
        #             for row in participateSet:
        #                 pid.append(row.pid)
        #         else:
        #             cid_not_in_participate.append(cid)

        #     for cid in cid_not_in_participate:
        #         del cid_dict[cid]
        if disease:
            clinicalTrialsQuery = ClinicalTrials.objects.filter(disease_detail__contains=disease)
            cid_list = [trial.cid for trial in clinicalTrialsQuery]
            pid_in_participate = []

            for cid in cid_list:
                tempQuery = Participate.objects.filter(cid=cid)
                participate_list = [p.pid.pid for p in tempQuery]
                pid_in_participate += participate_list

            pid_list = sorted((set(pid_list).intersection(pid_in_participate)))

        person = PersonSerializer(Person.objects.filter(pid__in=pid_list), many=True)
        return Response({
            'person': person.data
        })


class ClinicalTrialsAPI(APIView):
    def get(self, request):
        pid = request.GET.get('pid')
        participateQuery = Participate.objects.filter(pid=pid)
        participate = ParticipateSerializer(participateQuery, many=True)
        return Response(participate.data)


class ThesisAPI(APIView):
    def get(self, request):
        pid = request.GET.get('pid')
        writesQuery = Writes.objects.filter(pid=pid)
        writes = WritesSerializer(writesQuery, many=True)
        return Response(writes.data)


@api_view(['GET'])
def name_list(request):
    nameQuery = Person.objects.all().values('name_kor')
    name = NameSerializer(nameQuery, many=True)
    return Response(name.data)
    

@api_view(['GET'])
def hospital_list(request):
    hospitalQuery = Person.objects.all().values('belong').distinct()
    hospital = HospitalSerializer(hospitalQuery, many=True)
    return Response(hospital.data)


@api_view(['GET'])
def get_coworker(request):
    pid = request.GET.get('pid')
    writes = Writes.objects.filter(pid=pid)
    tid_list = [thesis.tid.tid for thesis in writes]

    coworker_list = []
    for tid in tid_list:
        thesis_title = Thesis.objects.get(tid=tid).title
        coworker = Thesis.objects.filter(title=thesis_title)
        if len(coworker) > 1:
            coworker_list.append(coworker[1])

    print(coworker_list)


    return Response(ThesisSerializer(coworker_list, many=True).data)