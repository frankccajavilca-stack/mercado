# apps/appointments/views.py

import os
import json
import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt
from dotenv import load_dotenv
from .models import Appointment
from .serializers import AppointmentSerializer
from django.utils.dateparse import parse_datetime
from django.utils import timezone
from django.conf import settings
from rest_framework.generics import ListAPIView

# --- IMPORTS ADICIONALES PARA LA INTEGRACIÓN DE PAGOS ---
from apps.payments.utils import create_mp_preference
from apps.payments.models import PaymentPreference
# -----------------------------------------------------


# Cargar .env
load_dotenv()

# Constantes GHL
GHL_BASE_URL = "https://services.leadconnectorhq.com"
GHL_API_VERSION = os.getenv("GHL_API_VERSION", "2021-04-15")
ACCESS_TOKEN = os.getenv("GHL_ACCESS_TOKEN")
GHL_LOCATION_ID = os.getenv("GHL_LOCATION_ID") 

if not ACCESS_TOKEN:
    raise Exception("Access Token de GHL no configurado en .env (GHL_ACCESS_TOKEN)")

def _to_datetime(iso_str):
    """Convierte ISO8601 string a datetime aware o devuelve None."""
    if not iso_str:
        return None
    dt = parse_datetime(iso_str)
    if dt is None:
        return None
    if settings.USE_TZ and timezone.is_naive(dt):
        tz = timezone.get_current_timezone()
        dt = timezone.make_aware(dt, tz)
    return dt

class AppointmentCreateView(APIView):
    """
    Crear una cita en GHL, guardarla en MySQL y generar un link de pago de Mercado Pago.
    """
    def post(self, request, *args, **kwargs):
        data = request.data or {}
        # AÑADIMOS 'payment_amount' como campo requerido para el pago
        required_fields = ["calendarId", "contactId", "startTime", "endTime", "payment_amount"] 
        
        for field in required_fields:
            if field not in data:
                return Response({"error": f"Falta el campo requerido: {field}"}, status=status.HTTP_400_BAD_REQUEST)

        location_id = data.get("locationId") or GHL_LOCATION_ID
        if not location_id:
            return Response({"error": "No se encontró locationId"}, status=status.HTTP_400_BAD_REQUEST)

        headers = {
            "Authorization": f"Bearer {ACCESS_TOKEN}",
            "Version": GHL_API_VERSION,
            "Content-Type": "application/json",
            "LocationId": location_id
        }

        api_payload = {
            "calendarId": data["calendarId"],
            "locationId": location_id,
            "contactId": data["contactId"],
            "startTime": data["startTime"],
            "endTime": data["endTime"],
            "title": data.get("title", "Cita con Requerimiento de Pago"),
            "appointmentStatus": data.get("appointmentStatus", "confirmed"),
            "assignedUserId": data.get("assignedUserId"),
            "ignoreFreeSlotValidation": True,
            "toNotify": True
        }

        try:
            # 1. Crear CITA en GHL
            resp = requests.post(f"{GHL_BASE_URL}/calendars/events/appointments", json=api_payload, headers=headers, timeout=15)
            resp.raise_for_status()
            ghl_data = resp.json()

            ghl_appointment_id = ghl_data.get("id")
            contact_id = ghl_data.get("contactId") or api_payload["contactId"]
            start_dt = _to_datetime(ghl_data.get("startTime") or api_payload["startTime"])
            end_dt = _to_datetime(ghl_data.get("endTime") or api_payload["endTime"])

            # 2. Guardar CITA en BD local
            appointment, created = Appointment.objects.update_or_create(
                ghl_id=ghl_appointment_id,
                defaults={
                    "location_id": ghl_data.get("locationId") or location_id,
                    "calendar_id": ghl_data.get("calendarId") or api_payload["calendarId"],
                    "contact_id": contact_id,
                    "title": ghl_data.get("title") or api_payload.get("title", "Cita"),
                    "appointment_status": ghl_data.get("appointmentStatus") or api_payload.get("appointmentStatus", "confirmed"),
                    "assigned_user_id": ghl_data.get("assignedUserId") or api_payload.get("assignedUserId"),
                    "notes": ghl_data.get("notes") or None,
                    "start_time": start_dt,
                    "end_time": end_dt,
                    "source": ghl_data.get("source")
                }
            )
            
            # --- 3. Generar Link de Pago de Mercado Pago (Integración) ---
            init_point = None
            preference_id = None
            
            amount = data["payment_amount"] 
            description = data.get("payment_description", f"Pago por cita: {appointment.title}")

            try:
                # LLAMADA A LA FUNCIÓN DE UTILITY DE PAGOS
                mp_data = create_mp_preference(ghl_appointment_id, amount, description)
                init_point = mp_data["init_point"]
                preference_id = mp_data["id"]
                
                # Guardar la preferencia en BD local (modelo PaymentPreference)
                PaymentPreference.objects.create(
                    appointment_ghl_id=ghl_appointment_id,
                    contact_id=contact_id,
                    amount=amount,
                    description=description,
                    preference_id=preference_id,
                    init_point=init_point,
                    status="pending"
                )
                print(f"✅ Link de pago MP creado: {init_point}")

            except Exception as mp_e:
                print("❌ Advertencia: No se pudo generar el link de pago MP. Detalles:", str(mp_e))

            # 4. Devolver respuesta
            serializer = AppointmentSerializer(appointment)
            response_data = serializer.data
            
            if init_point:
                 response_data["payment_link"] = init_point
                 response_data["payment_preference_id"] = preference_id
                 response_data["message"] = "Cita y link de pago creados."
            else:
                 response_data["message"] = "Cita creada. ERROR al generar link de pago."

            return Response(response_data, status=status.HTTP_201_CREATED)

        except requests.exceptions.HTTPError as http_err:
            resp = http_err.response
            details = resp.text if resp is not None else str(http_err)
            code = resp.status_code if resp is not None else 500
            return Response({"error": "Error HTTP al crear cita en GHL", "details": details}, status=code)
        except requests.exceptions.RequestException as e:
            return Response({"error": "Error conexión GHL", "details": str(e)}, status=status.HTTP_502_BAD_GATEWAY)
        except Exception as e:
            return Response({"error": "Error interno", "details": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# --- El resto de tus vistas (ghl_webhook, AppointmentUpdateView, etc.) se mantienen IGUAL. ---
@csrf_exempt
@api_view(['POST'])
def ghl_webhook(request):
    # ... (Tu código para manejar webhooks de GHL) ...
    # Se mantiene como lo tenías.
    
    event = request.data or {}
    print("=== Webhook recibido de GHL ===")
    print(json.dumps(event, indent=2, ensure_ascii=False))

    appointment_data = event.get("appointment") if "appointment" in event else event
    event_type = event.get("type") or request.headers.get("X-GHL-Event")
    ghl_id = appointment_data.get("id") if isinstance(appointment_data, dict) else None

    location_id = event.get("locationId") or (appointment_data.get("locationId") if isinstance(appointment_data, dict) else None) or GHL_LOCATION_ID

    if not isinstance(appointment_data, dict) or not ghl_id:
        return Response({"error": "Payload inválido: no se encontró appointment.id"}, status=status.HTTP_400_BAD_REQUEST)

    start_dt = _to_datetime(appointment_data.get("startTime"))
    end_dt = _to_datetime(appointment_data.get("endTime"))
    date_added_dt = _to_datetime(appointment_data.get("dateAdded"))
    date_updated_dt = _to_datetime(appointment_data.get("dateUpdated"))

    try:
        if event_type == "AppointmentDelete" or appointment_data.get("appointmentStatus") == "cancelled":
            Appointment.objects.filter(ghl_id=ghl_id).update(appointment_status="cancelled")
            print("🟡 Marcada como cancelled en BD:", ghl_id)
            return Response({"status": "cancelled", "ghl_id": ghl_id}, status=status.HTTP_200_OK)

        if event_type in ["AppointmentCreate", "AppointmentUpdate"] or appointment_data.get("id"):
            appointment, created = Appointment.objects.update_or_create(
                ghl_id=ghl_id,
                defaults={
                    "location_id": location_id,
                    "calendar_id": appointment_data.get("calendarId"),
                    "contact_id": appointment_data.get("contactId"),
                    "title": appointment_data.get("title"),
                    "appointment_status": appointment_data.get("appointmentStatus"),
                    "assigned_user_id": appointment_data.get("assignedUserId"),
                    "notes": appointment_data.get("notes") or None,
                    "start_time": start_dt,
                    "end_time": end_dt,
                    "source": appointment_data.get("source"),
                    #"date_added": date_added_dt,
                    "date_updated": date_updated_dt,
                }
            )
            print("✅ Guardada/actualizada en MySQL:", appointment.ghl_id)
            return Response({"status": "ok", "ghl_id": ghl_id}, status=status.HTTP_200_OK)

        print("⚠️ Evento no manejado:", event_type)
        return Response({"status": "ignored", "event_type": event_type}, status=status.HTTP_200_OK)

    except Exception as e:
        print("❌ Error al procesar webhook:", str(e))
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class AppointmentUpdateView(APIView):
    # ... (Tu código para AppointmentUpdateView) ...
    def put(self, request, appointment_id):
        appointment = Appointment.objects.filter(ghl_id=appointment_id).first()
        location_id = appointment.location_id if appointment else GHL_LOCATION_ID

        headers = {
            "Authorization": f"Bearer {ACCESS_TOKEN}",
            "Version": GHL_API_VERSION,
            "Content-Type": "application/json",
            "LocationId": location_id
        }
        url = f"{GHL_BASE_URL}/calendars/events/appointments/{appointment_id}"

        try:
            resp = requests.put(url, headers=headers, json=request.data, timeout=15)
            resp.raise_for_status()
            data = resp.json()
            start_dt = _to_datetime(data.get("startTime"))
            end_dt = _to_datetime(data.get("endTime"))

            Appointment.objects.filter(ghl_id=appointment_id).update(
                title=data.get("title"),
                appointment_status=data.get("appointmentStatus"),
                assigned_user_id=data.get("assignedUserId"),
                notes=data.get("notes") or None,
                start_time=start_dt,
                end_time=end_dt,
            )
            return Response(data, status=resp.status_code)
        except requests.exceptions.RequestException as e:
            return Response({"error": "Error al actualizar cita en GHL", "details": str(e)}, status=500)


class AppointmentDeleteView(APIView):
    # ... (Tu código para AppointmentDeleteView) ...
    def delete(self, request, appointment_id):
        appointment = Appointment.objects.filter(ghl_id=appointment_id).first()
        location_id = appointment.location_id if appointment else GHL_LOCATION_ID

        headers = {
            "Authorization": f"Bearer {ACCESS_TOKEN}",
            "Version": GHL_API_VERSION,
            "Content-Type": "application/json",
            "LocationId": location_id
        }
        url = f"{GHL_BASE_URL}/calendars/events/appointments/{appointment_id}"

        payload = {"appointmentStatus": "cancelled"}

        try:
            resp = requests.put(url, headers=headers, json=payload, timeout=15)
            print("PUT GHL status:", resp.status_code)
            print("PUT GHL body:", resp.text)
            resp.raise_for_status()
            Appointment.objects.filter(ghl_id=appointment_id).update(appointment_status="cancelled")
            return Response({"message": "Cita cancelada correctamente"}, status=resp.status_code)
        except requests.exceptions.RequestException as e:
            return Response({"error": "Error al cancelar cita en GHL", "details": str(e)}, status=500)

class AppointmentListView(ListAPIView):
    queryset = Appointment.objects.all().order_by('-start_time')
    serializer_class = AppointmentSerializer
