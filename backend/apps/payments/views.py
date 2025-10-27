# payments/views.py
import json
import requests
import os 
import logging
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from dotenv import load_dotenv


from .models import PaymentPreference 
from .utils import create_mp_preference, update_ghl_contact, get_mp_payment_info 

# Configuración de Logging
logger = logging.getLogger(__name__)

# Carga las variables de entorno 
load_dotenv()
MP_BASE_URL = os.getenv("MP_BASE_URL", "https://api.mercadopago.com")
MP_ACCESS_TOKEN = os.getenv("MP_ACCESS_TOKEN")

# --- 1. Endpoint para crear el link de pago ---

class PaymentCreateView(APIView):
    """
    POST /payments/create
    Genera un link de pago.
    """
    def post(self, request):
        data = request.data
        required_fields = ["appointmentId", "contactId", "amount", "description"]
        for field in required_fields:
            if field not in data:
                return Response({"error": f"Falta el campo requerido: {field}"}, status=status.HTTP_400_BAD_REQUEST)

        appointment_ghl_id = data["appointmentId"]
        amount = data["amount"]
        description = data["description"]
        contact_id = data["contactId"]
        
        # 1. Validar si ya existe una preferencia para esta cita
        if PaymentPreference.objects.filter(appointment_ghl_id=appointment_ghl_id).exists():
             return Response({"error": "Ya existe una preferencia de pago para esta cita."}, 
                             status=status.HTTP_409_CONFLICT)

        try:
            # 2. Llamar a Mercado Pago para crear la preferencia
            mp_data = create_mp_preference(appointment_ghl_id, amount, description)
            
            preference_id = mp_data["id"]
            init_point = mp_data["init_point"]
            
            # 3. Guardar en BD local
            PaymentPreference.objects.create(
                appointment_ghl_id=appointment_ghl_id,
                contact_id=contact_id,
                amount=amount,
                description=description,
                preference_id=preference_id,
                init_point=init_point,
                status="pending"
            )
            
            return Response({
                "message": "Preferencia creada correctamente.",
                "appointmentId": appointment_ghl_id,
                "preferenceId": preference_id,
                "init_point": init_point,
            }, status=status.HTTP_201_CREATED)

        except Exception as e:
            logger.error(f"Error al procesar PaymentCreateView: {e}")
            return Response({"error": "Error al procesar la solicitud", "details": str(e)}, 
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# --- 2. Webhook de Mercado Pago y Actualización GHL ---

# Usamos api_view en lugar de APIView para el webhook
@api_view(['POST'])
@permission_classes([AllowAny])
def mp_webhook(request):
    """
    Maneja las notificaciones de webhook de Mercado Pago, extrayendo el ID del Query String.
    """
    
    # Obtener los parámetros del Query String de MP (formato más común para notificaciones)
    resource_id = request.query_params.get('id') or request.query_params.get('data.id')
    topic = request.query_params.get('topic') or request.query_params.get('type')
    
    logger.info(f"MP Webhook recibido. Topic: {topic}, Resource ID: {resource_id}")

    # 1. Validación de Webhook
    if not resource_id or not topic:
        return Response({"message": "Webhook inválido o faltan parámetros."}, status=status.HTTP_400_BAD_REQUEST)
        
    try:
        if topic == 'payment':
            # 2. Obtener detalles del pago desde MP API (Manejado por get_mp_payment_info)
            payment_data = get_mp_payment_info(resource_id)
            
            if not payment_data:
                # Si el pago no se encuentra o hay un error al consultar MP (manejado en utils.py)
                logger.warning(f"Pago {resource_id} no encontrado en MP o error en consulta. Notificación omitida.")
                return Response({"message": "Pago no encontrado o error en consulta MP."}, status=status.HTTP_200_OK)

            mp_status = payment_data.get('status')
            external_reference = payment_data.get('external_reference')
            
            if external_reference and mp_status:
                
                # 3. Idempotencia: Verificar si el pago ya fue aprobado
                if PaymentPreference.objects.filter(payment_id=resource_id, status='approved').exists():
                    logger.info(f"🟡 Pago {resource_id} ya procesado y aprobado (Idempotencia).")
                    return Response({"message": "Ya procesado."}, status=status.HTTP_200_OK)

                # 4. Actualizar la base de datos local
                try:
                    preference = PaymentPreference.objects.get(appointment_ghl_id=external_reference)
                    
                    if mp_status == 'approved' and preference.status != 'approved':
                        preference.status = 'approved'
                        preference.payment_id = resource_id 
                        preference.save() 
                        logger.info(f"✅ Pago {resource_id} aprobado. BD local actualizada.")
                        
                        # 5. Actualizar GoHighLevel
                        try:
                            contact_id = preference.contact_id 
                            update_ghl_contact(contact_id, tags=["pago_confirmado"]) 
                            logger.info(f"Contacto GHL (ID: {contact_id}) taggeado.")
                        except requests.exceptions.HTTPError as e:
                            # Captura el error 401/400 de GHL (Tu token es inválido/sin scope)
                            logger.error(f"Error al actualizar contacto en GHL: {e}")
                            logger.error(f"❌ Error GHL: {e.response.text if e.response is not None else str(e)}")
                            # Continuamos y devolvemos 200 OK a MP, el fallo es solo de GHL.
                            pass 
                        except Exception as e:
                            logger.error(f"Error inesperado al llamar a GHL: {e}")
                            pass
                        
                    elif preference.status != mp_status:
                        # Si es un cambio de estado (pendiente, rechazado, etc.)
                        preference.status = mp_status
                        preference.payment_id = resource_id 
                        preference.save()
                        logger.info(f"🟡 Pago {resource_id} actualizado a estado: {mp_status}.")

                    return Response({"message": "Webhook procesado correctamente."}, status=status.HTTP_200_OK)

                except PaymentPreference.DoesNotExist:
                    logger.warning(f"No se encontró PaymentPreference para external_reference: {external_reference}")
                    return Response({"message": "No se encontró preferencia local."}, status=status.HTTP_200_OK)
                except Exception as e:
                    # Otros errores de DB/lógica
                    logger.error(f"Error al buscar/actualizar preferencia en DB: {e}", exc_info=True)
                    return Response({"message": "Error de DB, reintento omitido."}, status=status.HTTP_200_OK)
            else:
                logger.error(f"Faltan datos clave en la respuesta de MP para el pago {resource_id}.")
                return Response({"message": "Datos de MP incompletos, notificación omitida."}, status=status.HTTP_200_OK)

        elif topic == 'merchant_order':
            logger.info(f"Merchant Order {resource_id} recibido y aceptado.")
            return Response({"message": "Merchant Order recibido y aceptado."}, status=status.HTTP_200_OK)

        else:
            return Response({"message": f"Topic {topic} no soportado."}, status=status.HTTP_200_OK)

    except Exception as e:
        logger.error(f"Error crítico al procesar webhook de MP: {e}", exc_info=True)
        # Devolver 200 OK para evitar reintentos de MP por errores internos
        return Response({"message": "Error crítico, reintento omitido."}, status=status.HTTP_200_OK)

# --- 3. Vista de Redirección de Éxito ---

class PaymentSuccessView(APIView):
    """Pago Completado."""
    def get(self, request, *args, **kwargs):
        payment_id = request.query_params.get('payment_id', 'N/A')
        
        context = {
            'payment_id': payment_id,
            'message': '¡Tu pago ha sido aprobado!',
            'details': 'Recibirás una confirmación por correo.'
        }
        
        # Devuelve JSON (ideal para APIs) o si estás usando templates, usa render.
        # Si estás usando APIView, Response es la mejor opción.
        return Response(context, status=status.HTTP_200_OK)

        # Si decides usar templates:
        # return render(request, 'payments/success.html', context)

from django.db.models import Count
from django.http import JsonResponse
from .models import PaymentPreference

def payment_summary(request):
    # Contar el total de pagos
    total_payments = PaymentPreference.objects.count()

    # Contar por estado (approved, rejected, pending, cancelled)
    status_counts = (
        PaymentPreference.objects
        .values('status')
        .annotate(total=Count('status'))
    )

    # Convertir el resultado a un diccionario más claro
    summary = {item['status']: item['total'] for item in status_counts}

    return JsonResponse({
        "total": total_payments,
        "approved": summary.get('approved', 0),
        "rejected": summary.get('rejected', 0),
        "pending": summary.get('pending', 0),
        "cancelled": summary.get('cancelled', 0),
    })

