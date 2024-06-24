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

class Query(graphene.ObjectType):
    all_orders = graphene.List(OrderType)
    all_order_items = graphene.List(Order_itemType)
    all_customers = graphene.List(CustomerType)
    all_parts = graphene.List(PartType)

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
    def resolve_all_parts(self, info, **kwargs):
        return Part.objects.all()

schema = graphene.Schema(query=Query)
