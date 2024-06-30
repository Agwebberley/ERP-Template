import graphene
from graphene_django.types import DjangoObjectType
from graphene_django_optimizer import resolver_hints
from core.models import Order, Order_item, Customer, Part



class OrderType(DjangoObjectType):
    class Meta:
        model = Order



class Order_itemType(DjangoObjectType):
    class Meta:
        model = Order_item



class CustomerType(DjangoObjectType):
    class Meta:
        model = Customer



class PartType(DjangoObjectType):
    class Meta:
        model = Part

class OffsetPaging(graphene.InputObjectType):
    offset = graphene.Int(description="Offset from the start.")
    limit = graphene.Int(description="Number of items to retrieve.")

class PartPagination(graphene.ObjectType):
    totalCount = graphene.Int()
    nodes = graphene.List(PartType)

    def resolve_totalCount(self, info):
        # Assuming Part.objects provides a way to count all items
        return Part.objects.count()

    def resolve_nodes(self, info, paging=None, **kwargs):
        queryset = Part.objects.all()
        if paging:
            offset = paging.get('offset', 0)
            limit = paging.get('limit', 10)
            queryset = queryset[offset:offset+limit]
        return queryset

class PartFilter(graphene.InputObjectType):
    name = graphene.String(description="Filter parts by name.")

class PartSort(graphene.Enum):
    NAME_ASC = "name"
    NAME_DESC = "-name"

class Query(graphene.ObjectType):
    all_orders = graphene.List(OrderType)
    all_order_items = graphene.List(Order_itemType)
    all_customers = graphene.List(CustomerType)
    all_parts = graphene.Field(
        PartPagination,
        paging=graphene.Argument(OffsetPaging),
        filters=graphene.Argument(PartFilter),
        sort=graphene.Argument(PartSort)
    )

    @resolver_hints(model_field='orders')
    def resolve_all_orders(self, info, **kwargs):
        return Order.objects.all()

    @resolver_hints(model_field='order_items')
    def resolve_all_order_items(self, info, **kwargs):
        return Order_item.objects.all()

    @resolver_hints(model_field='customers')
    def resolve_all_customers(self, info, **kwargs):
        return Customer.objects.all()

    @resolver_hints(model_field='parts')
    def resolve_all_parts(self, info, filters=None, sort=None, **kwargs):
        queryset = Part.objects.all()
        if filters and filters.get('name'):
            queryset = queryset.filter(name=filters['name'])
        if sort:
            queryset = queryset.order_by(sort)
        return queryset

schema = graphene.Schema(query=Query)
