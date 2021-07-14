from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import ClinicalTrials, Doctor, Person, Participate, Writes
from .serializers import ClinicalTrialsSerializer, DoctorSerializer, PersonSerializer, ParticipateSerializer, WritesSerializer
from itertools import chain
# Create your views here.

class DoctorTest(APIView):
    def get(self, request):
        queryset = Doctor.objects.all()
        serializer = DoctorSerializer(queryset, many=True)
        return Response(serializer.data)

class SearchName(APIView):
    def get(self, request):
        personPidQuery = Person.objects.filter(name_kor__contains=request.GET.get('doctor_name'))

        # personQuery = Person.objects.none()
        doctorQuery = Doctor.objects.none()
        participateQuery = Participate.objects.none()
        writesQuery = Writes.objects.none()
        # person_list = []
        # doctor_list = []
        # participate_list = []
        # writes_list = []
        for person in personPidQuery:
            # personQuery |= Person.objects.get(pid=person.pid)
            # doctorQuery |= Doctor.objects.get(pid_id=person.pid)
            # participateQuery |= Participate.objects.filter(pid=person.pid)
            # writesQuery |= Writes.objects.filter(pid=person.pid)

            # personQuery = chain(Person.objects.filter(pid=person.pid), personQuery)
            doctorQuery = chain(Doctor.objects.filter(pid_id=person.pid), doctorQuery)
            participateQuery = chain(Participate.objects.filter(pid=person.pid), participateQuery)
            writesQuery = chain(Writes.objects.filter(pid=person.pid), writesQuery)
            
        # person = PersonSerializer(personPidQuery, many=True)
        doctor = DoctorSerializer(doctorQuery, many=True)
        participation = ParticipateSerializer(participateQuery, many=True)
        writes = WritesSerializer(writesQuery, many=True)
        return Response({
            # 'person': person.data,
            'doctor_info': doctor.data,
            'participate': participation.data,
            'writes': writes.data
        }) 