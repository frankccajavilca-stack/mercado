import logging
from django.core.mail import send_mail
from django.conf import settings

logger = logging.getLogger(__name__)

def notify_error(subject, message):
    logger.error(f"[ALERTA] {subject}: {message}")
    try:
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=["admin@tusistema.com"],
            fail_silently=True,
        )
    except Exception as e:
        logger.error(f"Error enviando alerta: {e}")
