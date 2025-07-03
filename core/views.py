from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import LoginForm
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q
from app_interventions.models import Intervention
from .decorators import role_required

def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    form = LoginForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, "Nom d'utilisateur ou mot de passe invalide.")

    return render(request, 'core/login.html', {'form': form})

@login_required
def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
@role_required('admin')
def dashboard_view(request):
    kpis = Intervention.objects.aggregate(
        total=Count('id'),
        en_cours=Count('id', filter=Q(statut='en_cours')),
        en_retard=Count('id', filter=Q(statut='en_retard')),
        a_venir=Count('id', filter=Q(statut='planifiée')),
    )
    if kpis['en_retard'] and kpis['en_retard'] > 5:
        messages.warning(request, "Attention : de nombreuses interventions sont en retard !")
    return render(request, 'dashboard.html', kpis)
