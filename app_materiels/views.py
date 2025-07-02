from django.shortcuts import render, redirect, get_object_or_404
from .models import Materiel
from .forms import MaterielForm

def materiel_list(request):
    materiels = Materiel.objects.all()
    return render(request, 'app_materiels/materiel_list.html', {'materiels': materiels})

def materiel_create(request):
    if request.method == 'POST':
        form = MaterielForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('materiel_list')
    else:
        form = MaterielForm()
    return render(request, 'app_materiels/materiel_form.html', {'form': form})

def materiel_update(request, pk):
    materiel = get_object_or_404(Materiel, pk=pk)
    if request.method == 'POST':
        form = MaterielForm(request.POST, instance=materiel)
        if form.is_valid():
            form.save()
            return redirect('materiel_list')
    else:
        form = MaterielForm(instance=materiel)
    return render(request, 'app_materiels/materiel_form.html', {'form': form})

def materiel_delete(request, pk):
    materiel = get_object_or_404(Materiel, pk=pk)
    if request.method == 'POST':
        materiel.delete()
        return redirect('materiel_list')
    return render(request, 'app_materiels/materiel_confirm_delete.html', {'materiel': materiel})
