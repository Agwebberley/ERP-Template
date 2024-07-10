from django.db import models
from core.models import BaseModel
from orders.models import Order

class Invoice(BaseModel):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('PAID', 'Paid'),
        ('CANCELLED', 'Cancelled'),
    ]

    id = models.AutoField(primary_key=True)
    order = models.OneToOneField(Order, on_delete=models.CASCADE)
    invoice_date = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')

    def __str__(self):
        return f"Invoice {self.id} for {self.order} - {self.get_status_display()}"

    @property
    def total(self):
        return self.order.total