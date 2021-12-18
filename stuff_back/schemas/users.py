import graphene
import graphql_jwt
from graphene import relay, ObjectType
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as lg, logout

from ..models import *
from .general import UserNode


class UserLoginMutation(graphene.Mutation):
    class Arguments:
        login = graphene.String(required=True)
        password = graphene.String(required=True)

    current_user = graphene.Field(
        UserNode,
    )

    @classmethod
    def mutate(cls, root, info, login, password):
        user = authenticate(username=login, password=password)
        if user is not None:
            print(root)
            print(info.context)
            lg(info.context, user)
            return UserLoginMutation(current_user=user)
        else:
            raise Exception("Invalid login or password / user does not exist")


class UserLogoutMutation(graphene.Mutation):
    logout_user = graphene.Field(UserNode)

    @classmethod
    def mutate(cls, root, info):
        if info.context.user.is_authenticated:
            user = info.context.user
            logout(info.context)
            return UserLogoutMutation(logout_user=user)
        else:
            raise Exception("Not logged in")


class UserCreateMutation(graphene.Mutation):
    current_user = graphene.Field(UserNode)

    class Arguments:
        login = graphene.String(required=True)
        password = graphene.String(required=True)
        first_name = graphene.String(required=True)

    @classmethod
    def mutate(cls, root, info, login, password, first_name):
        user = authenticate(info.context, username=login, password=password)
        if user is not None:
            raise Exception("User already exists")
        else:
            user = User.objects.create(username=login, password=password, first_name=first_name, email=login)

            # это очень страшно, но дедлайн есть дедлайн
            Location.objects.create(name="Дом", loc_owner=user)
            Group.objects.create(name='Джинсы', gr_owner=user)
            Group.objects.create(name='Носки', gr_owner=user)
            Group.objects.create(name='Куртки', gr_owner=user)

            lg(info.context, user, backend="graphql_jwt.backends.JSONWebTokenBackend")
            return UserCreateMutation(current_user=user)

