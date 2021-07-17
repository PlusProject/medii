from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import ClinicalTrials, Doctor, Person, Participate, Writes
from .serializers import ClinicalTrialsSerializer, DoctorSerializer, PersonSerializer, ParticipateSerializer, WritesSerializer
from itertools import chain
from django.db.models import Q
# Create your views here.

class DoctorTest(APIView):
    def get(self, request):
        queryset = Doctor.objects.all()
        serializer = DoctorSerializer(queryset, many=True)
        return Response(serializer.data)

class SearchName(APIView):
    def get(self, request):
        name = request.GET.get('doctor_name')
        hospital = request.GET.get('hospital')
        personQuery = Person.objects.filter(name_kor__contains=name, belong__contains=hospital)
        # if name and hospital:
        #     personQuery = Person.objects.filter(name_kor__contains=name, belong__contains=hospital)
        #         # Q(name_kor__contains=name) |
        #         # Q(belong__contains=hospital)
        #         # ).distinct()
        # elif name:
        #     personQuery = Person.objects.filter(name_kor__contains=name)
        # else:
        #     personQuery = Person.objects.filter(belong__contains=hospital)

        # personQuery = Person.objects.none()
        doctorQuery = Doctor.objects.none()
        participateQuery = Participate.objects.none()
        writesQuery = Writes.objects.none()

        for person in personQuery:
            # personQuery = chain(Person.objects.filter(pid=person.pid), personQuery)
            doctorQuery = chain(Doctor.objects.filter(pid_id=person.pid), doctorQuery)
            participateQuery = chain(Participate.objects.filter(pid=person.pid), participateQuery)
            writesQuery = chain(Writes.objects.filter(pid=person.pid), writesQuery)
            
        person = PersonSerializer(personQuery, many=True)
        doctor = DoctorSerializer(doctorQuery, many=True)
        participation = ParticipateSerializer(participateQuery, many=True)
        writes = WritesSerializer(writesQuery, many=True)
        return Response({
            'person': person.data,
            'doctor_info': doctor.data,
            'participate': participation.data,
            'writes': writes.data
        })



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

        participateQuery = Participate.objects.none()
        writesQuery = Writes.objects.none()

        person_index = 0
        person = PersonSerializer(Person.objects.filter(pid__in=pid_list), many=True)

        for pid in pid_list:
            participateQuery = Participate.objects.filter(pid=pid)
            writesQuery = Writes.objects.filter(pid=pid)
            person.data[person_index]['participate_num'] = participateQuery.count()
            person.data[person_index]['thesis_num'] = writesQuery.count()

            if disease:
            #     disease_cid = ''
            #     a = 0
            #     for key, value in cid_dict.items():
            #         disease_cid += '|' + str(key)
            #         # if pid in value:
            #         #     disease_cid.append(key)
            #         #     a = pid
            #     
                person.data[person_index]['related_cid'] = pid_in_participate
            person_index += 1
        
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