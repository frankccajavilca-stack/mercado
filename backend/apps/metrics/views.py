#backend/apps/metrics/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from apps.appointments.models import Appointment
import logging

logger = logging.getLogger(__name__)

class MetricsOverviewView(APIView):
    """
    Endpoint /metrics/overview
    Devuelve métricas locales sobre citas con tag pago_confirmado
    """
    def get(self, request):
        try:
            total_citas = Appointment.objects.count()
            citas_confirmadas = Appointment.objects.filter(appointment_status="confirmed").count()
            citas_pago_confirmado = Appointment.objects.filter(tags__contains=["pago_confirmado"]).count()

            data = {
                "total_citas": total_citas,
                "confirmadas": citas_confirmadas,
                "pago_confirmado": citas_pago_confirmado,
            }

            # Alerta si no hay citas con pago_confirmado
            if citas_pago_confirmado == 0:
                logger.warning("⚠️ No hay citas con pago_confirmado registradas.")

            return Response(data, status=status.HTTP_200_OK)

        except Exception as e:
            logger.error(f"Error en /metrics/overview: {e}")
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)




