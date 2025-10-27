# /payments/utils.py
import os
import requests
import json
from dotenv import load_dotenv

# Cargar .env
load_dotenv()

# Constantes de GHL
GHL_BASE_URL = "https://services.leadconnectorhq.com"
GHL_API_VERSION = os.getenv("GHL_API_VERSION", "2021-04-15")
GHL_ACCESS_TOKEN = os.getenv("GHL_ACCESS_TOKEN")
GHL_LOCATION_ID = os.getenv("GHL_LOCATION_ID")

# Constantes de Mercado Pago
MP_BASE_URL = os.getenv("MP_BASE_URL", "https://api.mercadopago.com")
MP_ACCESS_TOKEN = os.getenv("MP_ACCESS_TOKEN")
PUBLIC_WEBHOOK_URL = os.getenv("PUBLIC_WEBHOOK_URL")

# --- Funciones de Mercado Pago ---

def get_mp_payment_info(resource_id):
    """
    Consulta a la API de MP para obtener detalles del pago.
    Devuelve el JSON de pago o None si no se encuentra.
    """
    if not MP_ACCESS_TOKEN:
        print("Error: Falta MP_ACCESS_TOKEN para consultar detalles de pago.")
        return None
        
    headers = {
        "Authorization": f"Bearer {MP_ACCESS_TOKEN}",
        "Content-Type": "application/json",
    }
    
    # Endpoint de consulta de pagos
    url = f"{MP_BASE_URL}/v1/payments/{resource_id}"
    
    try:
        resp = requests.get(url, headers=headers, timeout=15)
        
        if resp.status_code == 404:
            # Maneja correctamente el caso donde el pago no existe (como tu ID de prueba '123456')
            print(f"Advertencia: Pago ID {resource_id} no encontrado en Mercado Pago (404).")
            return None
            
        resp.raise_for_status() # Lanza HTTPError para 4xx o 5xx (excepto 404)
        return resp.json()
        
    except requests.exceptions.RequestException as e:
        print(f"Error al consultar detalles de pago {resource_id} en MP: {e}")
        return None


def create_mp_preference(appointment_ghl_id, amount, description):
    """Llama a la API de Mercado Pago para crear una preferencia de pago."""
    if not MP_ACCESS_TOKEN or not PUBLIC_WEBHOOK_URL:
        raise Exception("Faltan variables de entorno de Mercado Pago (MP_ACCESS_TOKEN, PUBLIC_WEBHOOK_URL)")
    
    headers = {
        "Authorization": f"Bearer {MP_ACCESS_TOKEN}",
        "Content-Type": "application/json",
    }
    
    # 1. URL DEL WEBHOOK (Para la notificación)
    notification_url = f"{PUBLIC_WEBHOOK_URL}/api/payments/webhooks/mp/"
    
    # 2. URLs DE REDIRECCIÓN (Para el usuario después del pago)
    # Estas rutas deben coincidir con las rutas raíz definidas en reflexoperu/urls.py
    SUCCESS_URL = f"{PUBLIC_WEBHOOK_URL}/payment-success/"
    PENDING_URL = f"{PUBLIC_WEBHOOK_URL}/payment-pending/"
    FAILURE_URL = f"{PUBLIC_WEBHOOK_URL}/payment-failure/"

    payload = {
        "items": [
            {
                "title": description,
                "quantity": 1,
                "unit_price": float(amount),
                "currency_id": "PEN" # Asegúrate de usar la moneda correcta
            }
        ],
        "external_reference": appointment_ghl_id, # Usamos el ID de la cita GHL como referencia externa
        "notification_url": notification_url,
        
        "back_urls": { 
            "success": SUCCESS_URL,
            "pending": PENDING_URL,
            "failure": FAILURE_URL
        },
        "auto_return": "approved"
    }

    try:
        url = f"{MP_BASE_URL}/checkout/preferences"
        resp = requests.post(url, headers=headers, json=payload, timeout=15)
        resp.raise_for_status()
        return resp.json()
    except requests.exceptions.RequestException as e:
        print(f"Error al crear preferencia en MP: {e}")
        details = resp.text if resp is not None else str(e)
        raise Exception(f"Error en MP: {details}")

# --- Funciones de GoHighLevel ---

def update_ghl_contact(contact_id, tags=None, custom_fields=None):
    """Actualiza un contacto en GHL (agregar tag o custom field)."""
    if not GHL_ACCESS_TOKEN or not GHL_LOCATION_ID:
        raise Exception("Faltan variables de entorno de GHL (GHL_ACCESS_TOKEN, GHL_LOCATION_ID)")
    
    headers = {
        "Authorization": f"Bearer {GHL_ACCESS_TOKEN}",
        "Version": GHL_API_VERSION,
        "Content-Type": "application/json",
        "LocationId": GHL_LOCATION_ID
    }

    url = f"{GHL_BASE_URL}/contacts/{contact_id}"
    
    payload = {}
    if tags is not None:
        payload["tags"] = tags 
    if custom_fields is not None:
        payload["customField"] = custom_fields 

    if not payload:
        return {"message": "No hay datos para actualizar."}

    try:
        resp = requests.put(url, headers=headers, json=payload, timeout=15)
        resp.raise_for_status()
        return resp.json()
    except requests.exceptions.RequestException as e:
        print(f"Error al actualizar contacto en GHL: {e}")
        details = resp.text if resp is not None else str(e)
        raise Exception(f"Error en GHL: {details}")