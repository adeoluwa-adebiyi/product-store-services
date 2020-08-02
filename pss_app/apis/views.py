from django.shortcuts import render

# Create your views here.
from graphene import ObjectType
from graphene_django.tests.schema import Query
from graphene_django.views import GraphQLView
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
import graphene

from apis.queries.product import ProductQuery


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


schema = graphene.Schema(query=RootQuery)
