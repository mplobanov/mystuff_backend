import graphene
from django.forms import ModelForm
from graphene_django.forms.mutation import DjangoModelFormMutation
from graphql_relay import from_global_id

from .general import *


def custom_mutate(cls, form, info, owner_property, Model):
    if not info.context.user.is_authenticated:
        raise Exception('Not logged in')
    if 'client_mutation_id' in form.data.keys():
        idd = from_global_id(form.data['client_mutation_id'])[1]
        print(form.cleaned_data, idd)
        obj = Model.objects.get(pk=idd)
        for k, v in form.cleaned_data.items():
            setattr(obj, k, v)
        if getattr(obj, owner_property) != info.context.user:
            raise Exception("403 Forbidden")
    else:
        obj = form.save(commit=False)
        setattr(obj, owner_property, info.context.user)
    obj.save()
    kwargs = {cls._meta.return_field_name: obj}
    return cls(errors=[], **kwargs)


class LocationForm(ModelForm):
    class Meta:
        model = Location
        exclude = ['loc_owner']


class LocationMutation(DjangoModelFormMutation):
    class Meta:
        form_class = LocationForm

    @classmethod
    def perform_mutate(cls, form, info):
        return custom_mutate(cls, form, info, 'loc_owner', Location)


class StatusForm(ModelForm):
    class Meta:
        model = Status
        exclude = ['st_owner']


class StatusMutation(DjangoModelFormMutation):
    class Meta:
        form_class = StatusForm

    @classmethod
    def perform_mutate(cls, form, info):
        return custom_mutate(cls, form, info, 'st_owner', Status)


class GroupForm(ModelForm):
    class Meta:
        model = Group
        exclude = ['gr_owner']


class GroupMutation(DjangoModelFormMutation):
    class Meta:
        form_class = GroupForm

    @classmethod
    def perform_mutate(cls, form, info):
        return custom_mutate(cls, form, info, 'gr_owner', Group)


class ItemMutationInput(graphene.InputObjectType):
    id = graphene.String()
    name = graphene.String(required=True)

    brand = graphene.String(required=True)
    color = graphene.String(required=True)
    size = graphene.String(required=True)
    volume = graphene.String(required=True)

    status = graphene.GlobalID(required=True)
    location = graphene.GlobalID(required=True)
    group = graphene.GlobalID(required=True)


class ItemMutation(graphene.Mutation):
    class Arguments:
        input = ItemMutationInput(required=True)

    item = graphene.Field(ItemNode)

    @staticmethod
    def mutate(root, info, input):
        if not info.context.user.is_authenticated:
            raise Exception('Not logged in')
        if Location.objects.get(pk=from_global_id(input['location'])[1]).loc_owner != info.context.user:
            raise Exception('403 Forbidden Location')
        if Status.objects.get(pk=from_global_id(input['status'])[1]).st_owner != info.context.user:
            raise Exception('403 Forbidden Status')
        if Group.objects.get(pk=from_global_id(input['group'])[1]).gr_owner != info.context.user:
            raise Exception('403 Forbidden Group')
        if 'id' in input.keys():
            item = Item.objects.get(pk=from_global_id(input['id'])[1])
            if item.owner != info.context.user:
                raise Exception('403 Forbidden')
            for key in ['name', 'brand', 'color', 'size', 'volume']:
                setattr(item, key, input[key])
            for key in ['location', 'status', 'group']:
                setattr(item, "{}_id".format(key), from_global_id(input[key])[1])
            item.save()
        else:
            if not input['name']:
                raise Exception("Name required")
            item = Item.objects.create(
                name=input['name'],

                brand=input['brand'],
                color=input['color'],
                size=input['size'],
                volume=input['volume'],

                location_id=from_global_id(input['location'])[1],
                status_id=from_global_id(input['status'])[1],
                group_id=from_global_id(input['group'])[1],

                owner_id=info.context.user.id
            )

        return ItemMutation(item=item)

