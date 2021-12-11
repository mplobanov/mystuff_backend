from django.forms import ModelForm
from graphene_django.forms.mutation import DjangoModelFormMutation
from graphql_relay import from_global_id

from .general import *


def custom_mutate(cls, form, info, owner_property, Model):
    if not info.context.user.is_authenticated:
        raise Exception('Not logged in')
    if 'client_mutation_id' in form.data.keys():
        idd = from_global_id(form.data['client_mutation_id'])[1]
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


class ItemForm(ModelForm):
    class Meta:
        model = Item
        exclude = ['owner']


class ItemMutation(DjangoModelFormMutation):
    class Meta:
        form_class = ItemForm

    @classmethod
    def perform_mutate(cls, form, info):
        return custom_mutate(cls, form, info, 'owner', Item)
