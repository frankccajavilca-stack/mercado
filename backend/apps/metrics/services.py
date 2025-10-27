
# apps/metrics/services.py
import logging
import requests
from django.conf import settings

logger = logging.getLogger(__name__)

def get_ghl_confirmed_appointments():
    """
    Consulta las citas desde GoHighLevel (GHL)
    y devuelve cuántas tienen el tag 'pago_confirmado'.
    """
    GHL_API_URL = "https://services.leadconnectorhq.com/calendars/events/appointments"

    headers = {
        "Authorization": f"Bearer {settings.GHL_API_KEY}",
        "Version": "2021-04-15"
    }

    params = {
        "locationId": settings.GHL_LOCATION_ID,
        "calendarId": settings.GHL_CALENDAR_ID,
    }

    try:
        response = requests.get(GHL_API_URL, headers=headers, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        citas_confirmadas = [
            cita for cita in data.get("appointments", [])
            if "pago_confirmado" in (cita.get("tags") or [])
        ]

        logger.info(f"✅ {len(citas_confirmadas)} citas con tag 'pago_confirmado'")
        return len(citas_confirmadas)

    except requests.RequestException as e:
        logger.error(f"❌ Error al consultar GHL: {e}")
        return 0

