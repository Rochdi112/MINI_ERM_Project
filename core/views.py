from django.shortcuts import render
from app_clients.models import Client
from app_techniciens.models import Technicien
from app_interventions.models import Intervention

def dashboard_view(request):
    context = {
        "clients_count": Client.objects.count(),
        "techniciens_count": Technicien.objects.count(),
        "interventions_count": Intervention.objects.count(),
    }
    return render(request, "dashboard.html", context)
