from django.shortcuts import render
from .serializers import TestimonialSerializer
from .models import Testimonial
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

# Create your views here.

class TestimonialListView(APIView):
    serializer_class=TestimonialSerializer
    def get(self, request):
        testimonials=Testimonial.objects.all()
        serializer = self.serializer_class(testimonials, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)