from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView


class Order(APIView):

    authentication_classes = ()
    permission_classes = ()

    def post(self, request):
        pass