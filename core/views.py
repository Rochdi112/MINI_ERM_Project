from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import LoginForm
from .models import ProfilUtilisateur

def login_view(request):
    form = LoginForm(request.POST or None)
    error = None

    if request.method == 'POST':
        if form.is_valid():
            user = authenticate(
                request,
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password']
            )
            if user:
                login(request, user)
                profil = ProfilUtilisateur.objects.get(user=user)
                if profil.role == 'admin':
                    return redirect('dashboard')
                elif profil.role == 'technicien':
                    return redirect('intervention_list')
                else:
                    return redirect('client_home')
            else:
                error = "Identifiants incorrects."

    return render(request, 'core/login.html', {'form': form, 'error': error})

@login_required
def logout_view(request):
    logout(request)
    return redirect('login')
