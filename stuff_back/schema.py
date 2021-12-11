from .schemas.mutations import *
from .schemas.users import *


class Query(graphene.ObjectType):
    location = relay.Node.Field(LocationNode)
    all_locations = DjangoFilterConnectionField(LocationNode)

    def resolve_all_locations(root, info):
        if info.context.user.is_authenticated:
            return Location.objects.filter(loc_owner=info.context.user)
        else:
            return Location.objects.none()

    status = relay.Node.Field(StatusNode)
    all_statuses = DjangoFilterConnectionField(StatusNode)

    def resolve_all_statuses(root, info):
        if info.context.user.is_authenticated:
            return Status.objects.filter(st_owner=info.context.user)
        else:
            return Status.objects.none()

    item = relay.Node.Field(ItemNode)
    all_items = DjangoFilterConnectionField(ItemNode)

    def resolve_all_items(root, info):
        if info.context.user.is_authenticated:
            return Item.objects.filter(owner=info.context.user)
        else:
            return Item.objects.none()

    group = relay.Node.Field(GroupNode)
    all_groups = DjangoFilterConnectionField(GroupNode)

    def resolve_all_groups(root, info):
        if info.context.user.is_authenticated:
            return Group.objects.filter(gr_owner=info.context.user)
        else:
            return Group.objects.none()

    current_user = graphene.Field(
        UserNode,
    )

    def resolve_current_user(root, info):
        if info.context.user.is_authenticated:
            res = User.objects.get(pk=info.context.user.pk)
            if res:
                return res
            else:
                return None
        else:
            return None


class Mutation(graphene.ObjectType):
    login = UserLoginMutation.Field()
    logout = UserLogoutMutation.Field()
    register = UserCreateMutation.Field()

    add_location = LocationMutation.Field()
    edit_location = LocationMutation.Field()
    add_item = ItemMutation.Field()
    edit_item = ItemMutation.Field()
    add_group = GroupMutation.Field()
    edit_group = GroupMutation.Field()
    add_status = StatusMutation.Field()
    edit_status = StatusMutation.Field()

