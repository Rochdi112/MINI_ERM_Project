from django.urls import path
from .views import dashboard, dashboard_kpi_htmx

app_name = 'dashboard'

urlpatterns = [
    path('', dashboard, name='dashboard'),
    path('htmx-kpi/', dashboard_kpi_htmx, name='htmx-kpi'),
]
