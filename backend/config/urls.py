"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
# Importa la vista de éxito directamente al archivo principal
from apps.payments.views import PaymentSuccessView 

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # --- RUTAS DE API ---
    path('api/appointments/', include('apps.appointments.urls')), 
    path('api/payments/', include('apps.payments.urls')), # Aquí solo quedan: create/ y webhooks/mp/
    # -------------------
    
    # --- RUTAS DE REDIRECCIÓN DE USUARIO (NIVEL RAIZ) ---
    # Mercado Pago dirige aquí: /payment-success/
    path('payment-success/', PaymentSuccessView.as_view(), name='payment-success'),
     # 👇 agrega esta línea para rutas sin /api/
    path('payments/', include('apps.payments.urls')),
    # Asegúrate de agregar las de pending y failure también para evitar futuros 404s
    # path('payment-pending/', PaymentPendingView.as_view(), name='payment-pending'),
    # path('payment-failure/', PaymentFailureView.as_view(), name='payment-failure'),
    # ----------------------------------------------------
]

# --- RUTA PARA SERVIR REACT (PRODUCCIÓN) ---
#urlpatterns += [
    # cualquier ruta que no comience con /api/ servirá el build de React
 #   re_path(r"^(?!api/).*", TemplateView.as_view(template_name="index.html")),
#]