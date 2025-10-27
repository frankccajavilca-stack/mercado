# payments/models.py
from django.db import models
from django.utils import timezone

class PaymentPreference(models.Model):
    # Enlace a tus modelos (asumiendo que quieres enlazarlo con tu Appointment)
    appointment_ghl_id = models.CharField(max_length=100, unique=True, help_text="ID de GHL de la cita")
    contact_id = models.CharField(max_length=100, help_text="ID del Contacto en GHL")

    # Datos de Mercado Pago
    preference_id = models.CharField(max_length=100, unique=True, null=True, blank=True, help_text="ID de la Preferencia de MP")
    payment_id = models.CharField(max_length=100, unique=True, null=True, blank=True, help_text="ID del Pago real en MP (para idempotencia)")
    
    # URL de pago y monto
    init_point = models.URLField(max_length=500, null=True, blank=True, help_text="URL de Checkout Pro")
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.CharField(max_length=255)

    # Estado del pago
    STATUS_CHOICES = [
        ('pending', 'Pendiente'),
        ('approved', 'Aprobado'),
        ('rejected', 'Rechazado'),
        ('cancelled', 'Cancelado'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Preferencia de Pago MP"
        verbose_name_plural = "Preferencias de Pago MP"

    def __str__(self):
        return f"Pref: {self.preference_id} - Status: {self.status} - Appt: {self.appointment_ghl_id}"

    def __str__(self):
        return f"Pago {self.external_id} - {self.status}"
