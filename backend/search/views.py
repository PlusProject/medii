from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import ClinicalTrials, Doctor, Person, Participate, Writes
from .serializers import ClinicalTrialsSerializer, DoctorSerializer, PersonSerializer, ParticipateSerializer, WritesSerializer
from .serializers import serializers
# Create your views here.

class DoctorTest(APIView):
    def get(self, request):
        queryset = Doctor.objects.all()
        serializer = DoctorSerializer(queryset, many=True)
        return Response(serializer.data)

class SearchName(APIView):
    def get(self, request):
        personQuery = Person.objects.get(name_kor=request.GET.get('doctor_name'))
        person = PersonSerializer(personQuery)

        doctorQuery = Doctor.objects.get(pid=personQuery.pid)
        doctor = DoctorSerializer(doctorQuery)

        participateQuery = Participate.objects.filter(pid=personQuery.pid)
        participation = ParticipateSerializer(participateQuery, many=True)

        writesQuery = Writes.objects.filter(pid=personQuery.pid)
        writes = WritesSerializer(writesQuery, many=True)
        return Response({
            'person': person.data,
            'doctor_info': doctor.data,
            'participate': participation.data,
            'writes': writes.data
        })