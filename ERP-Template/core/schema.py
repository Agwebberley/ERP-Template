import graphene
from graphene_django.types import DjangoObjectType
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
    def resolve_all_orders(self, info, **kwargs):
        return Order.objects.all()

    all_order_items = graphene.List(Order_itemType)
    def resolve_all_order_items(self, info, **kwargs):
        return Order_item.objects.all()

    all_customers = graphene.List(CustomerType)
    def resolve_all_customers(self, info, **kwargs):
        return Customer.objects.all()

    all_parts = graphene.List(PartType)
    def resolve_all_parts(self, info, **kwargs):
        return Part.objects.all()

schema = graphene.Schema(query=Query)
