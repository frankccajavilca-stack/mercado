from django.core.management.base import BaseCommand
from apps.payments.models import PaymentPreference
from django.utils import timezone
import mercadopago

class Command(BaseCommand):
    help = 'Genera pagos de prueba simplificados en sandbox'

    def handle(self, *args, **kwargs):
        ACCESS_TOKEN = "TU_ACCESS_TOKEN_DE_PRUEBA"
        sdk = mercadopago.SDK(ACCESS_TOKEN)

        # Estados de prueba
        estados = ["approved", "pending", "rejected", "cancelled"]

        for estado in estados:
            # Crear pago
            payment_data = {
                "transaction_amount": 100.0,
                "description": f"Pago de prueba {estado}",
                "payment_method_id": "visa",
                "payer": {"email": "test_user_1234@test.com"},
                "status": "pending"  # Inicialmente pendiente
            }

            response = sdk.payment().create(payment_data)
            payment = response.get("response", {})

            # Si no hay 'id', imprimir error y continuar
            payment_id = payment.get("id", None)
            if not payment_id:
                self.stdout.write(self.style.ERROR(f"❌ No se pudo crear el pago para estado '{estado}'."))
                self.stdout.write(str(payment))
                continue

            # Actualizar al estado deseado
            sdk.payment().update(payment_id, {"status": estado})

            # Guardar en DB
            PaymentPreference.objects.create(
                payment_preference_id=payment_id,
                amount=payment.get("transaction_amount", 100.0),
                status=estado,
                description=f"Pago de prueba {estado}",
                date_added=timezone.now()
            )

        # Resumen final
        payments = PaymentPreference.objects.all()
        summary = {
            "total": payments.count(),
            "approved": payments.filter(status="approved").count(),
            "pending": payments.filter(status="pending").count(),
            "rejected": payments.filter(status="rejected").count(),
            "cancelled": payments.filter(status="cancelled").count(),
        }

        self.stdout.write("📊 Resumen de pagos en DB:")
        self.stdout.write(str(summary))
