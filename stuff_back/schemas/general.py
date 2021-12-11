from graphene import relay, ObjectType
from graphene_django import DjangoObjectType
from django.contrib.auth.models import User
from ..models import *


class LocationNode(DjangoObjectType):
    class Meta:
        model = Location
        filter_fields = '__all__'
        interfaces = (relay.Node,)


class StatusNode(DjangoObjectType):
    class Meta:
        model = Status
        filter_fields = '__all__'
        interfaces = (relay.Node,)


class GroupNode(DjangoObjectType):
    class Meta:
        model = Group
        filter_fields = '__all__'
        interfaces = (relay.Node,)


class UserNode(DjangoObjectType):
    class Meta:
        model = User
        filter_fields = '__all__'
        interfaces = (relay.Node,)


class ItemNode(DjangoObjectType):
    class Meta:
        model = Item
        filter_fields = "__all__"
        interfaces = (relay.Node,)