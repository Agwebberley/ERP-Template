import requests
from django.core.management.base import BaseCommand
from inventory.models import Part
from orders.models import Order, OrderItem
from customers.models import Customer
from random import randint

# "X-API-Key: ZlvoECeT1FbFpYMqWzB_Aw" https://random-data-api.com/api/v3/projects/8e5074e8-2f7c-479f-8764-cd327635c522

class Command(BaseCommand):
    def handle(self, *args, **options):
        url = "https://random-data-api.com/api/v3/projects/8e5074e8-2f7c-479f-8764-cd327635c522"
        headers = {"X-API-Key": "ZlvoECeT1FbFpYMqWzB_Aw"}

        response = requests.get(url, headers=headers)
        data = response.json()

        for part in data["part"]:
            Part.objects.create(
                name=part["product_name"],
                description=part["description"],
                part_number=part["part_number"],
                cost=part["cost"],
                price=part["price"],
                quantity=part["quantity"],
                reorder_level=part["reorder_level"]
            )
        for customer in data["customer"]:
            Customer.objects.create(
                name=customer["full_name"],
                email=customer["email"],
                phone=customer["phone"],
                address=customer["street_address"]
            )
        
        for order in range(10):
            customer = Customer.objects.order_by("?").first()
            order = Order.objects.create(customer=customer)
            for item in range(randint(1,10)):
                part = Part.objects.order_by("?").first()
                OrderItem.objects.create(order=order, part=part, quantity=randint(1, 10))