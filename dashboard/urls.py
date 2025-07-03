from django.urls import path
from .views import dashboard_kpi_htmx

app_name = 'dashboard'

urlpatterns = [
    path('htmx-kpi/', dashboard_kpi_htmx, name='htmx-kpi'),
]
