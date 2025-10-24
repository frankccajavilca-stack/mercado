from django.db import models
from django.utils import timezone

class Payment(models.Model):
    STATUS_CHOICES = [
        ('created', 'Creado'),
        ('approved', 'Aprobado'),
        ('rejected', 'Rechazado'),
        ('pending', 'Pendiente'),
    ]

    external_id = models.CharField(max_length=200, unique=True)  # ID Mercado Pago
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='created')
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Pago {self.external_id} - {self.status}"
