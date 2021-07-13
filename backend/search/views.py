from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Doctor, Person
from .serializers import DoctorSerializer
from .serializers import serializers
# Create your views here.

class DoctorTest(APIView):
    def get(self, request):
        queryset = Doctor.objects.all()
        serializer = DoctorSerializer(queryset, many=True)
        return Response(serializer.data)

class SearchName(APIView):
    def get(self, request):
        queryset = Person.objects.filter(name_kor=request.data['doctor_name'])
        serializer = DoctorSerializer(queryset, many=True)
        return Response(serializer.data)