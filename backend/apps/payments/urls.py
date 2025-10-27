from django.urls import path
from .views import PaymentCreateView, mp_webhook, payment_summary
urlpatterns = [
    path('create/', PaymentCreateView.as_view(), name='create_payment_link'),
    path('webhooks/mp/', mp_webhook, name='mercadopago_webhook'),
    path('summary/', payment_summary, name='payment_summary'),#nuevo
]
