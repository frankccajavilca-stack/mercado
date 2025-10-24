import logging
import requests

logger = logging.getLogger(__name__)

GHL_API_URL = "https://services.leadconnectorhq.com/calendars/events/appointments"
GHL_TOKEN = "TU_TOKEN_AQUI"  # ⚠️ Usa .env o settings seguros

def get_ghl_confirmed_appointments():
    headers = {
        "Authorization": f"Bearer {GHL_TOKEN}",
        "Version": "2021-04-15"
    }

    try:
        response = requests.get(GHL_API_URL, headers=headers)
        response.raise_for_status()
        data = response.json()

        citas_confirmadas = [
            cita for cita in data.get("appointments", [])
            if "pago_confirmado" in (cita.get("tags") or [])
        ]
        return len(citas_confirmadas)

    except requests.RequestException as e:
        logger.error(f"Error al consultar GHL: {e}")
        return 0
