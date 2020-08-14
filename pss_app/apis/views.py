import json

from django.shortcuts import render

# Create your views here.
from graphene import ObjectType
from graphene_django.tests.schema import Query
from graphene_django.views import GraphQLView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
import graphene

from apis.queries.product import ProductQuery

from apis.queries.checkout import RootMutation

from apis.models import Order

from apis.usecases.payment.payment_services import paystack_payment_service


class AppTitleType(ObjectType):
    name = graphene.String()


class RootQuery(ObjectType, ProductQuery):
    pass


class APIGqlView(APIView, GraphQLView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    @classmethod
    def as_view(cls, **initkwargs):
        return super().as_view(**initkwargs)


class PaymentHookProcessor(APIView):

    def post(self, request):
        print("WEBHOOK-POST:")
        print(json.dumps(request.data))
        paystack_payment_service.handle_webhook(json_data=request.data)
        return Response(status=status.HTTP_200_OK)


schema = graphene.Schema(query=RootQuery, mutation=RootMutation)
