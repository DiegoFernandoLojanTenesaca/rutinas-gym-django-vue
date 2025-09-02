import os
import requests

# Cargar variables de entorno
MAILTRAP_API_TOKEN = os.getenv("MAILTRAP_API_TOKEN")
MAILTRAP_INBOX_ID = os.getenv("MAILTRAP_INBOX_ID")
MAILTRAP_FROM_EMAIL = os.getenv("MAILTRAP_FROM_EMAIL", "hello@example.com")


def enviar_contacto_mailtrap_sandbox(asunto: str, html: str, destinatario: str) -> None:
    """
    Envía un correo de contacto usando la API de Mailtrap Sandbox.

    :param asunto: Asunto del correo
    :param html: Contenido HTML del correo
    :param destinatario: Dirección de email del receptor
    """

    if not MAILTRAP_API_TOKEN or not MAILTRAP_INBOX_ID:
        raise RuntimeError("Faltan MAILTRAP_API_TOKEN o MAILTRAP_INBOX_ID en .env")

    url = f"https://sandbox.api.mailtrap.io/api/send/{MAILTRAP_INBOX_ID}"
    headers = {
        "Authorization": f"Bearer {MAILTRAP_API_TOKEN}",
        "Content-Type": "application/json",
    }
    payload = {
        "from": {"email": MAILTRAP_FROM_EMAIL, "name": "Mailtrap Test"},
        "to": [{"email": destinatario}],
        "subject": asunto,
        "text": "Has recibido un nuevo mensaje de contacto.",
        "html": html,
        "category": "Integration Test"
    }

    try:
        resp = requests.post(url, json=payload, headers=headers, timeout=15)
        resp.raise_for_status()
    except requests.RequestException as e:
        print(f"[MAILTRAP SANDBOX API ERROR] {e}")
        if hasattr(e, "response") and e.response is not None:
            try:
                print(f"[MAILTRAP RESPONSE BODY] {e.response.text}")
            except Exception:
                pass
        raise
