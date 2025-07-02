from django.shortcuts import render, redirect, get_object_or_404
from .models import Technicien
from .forms import TechnicienForm

def technicien_list(request):
    techniciens = Technicien.objects.all()
    return render(request, 'app_techniciens/technicien_list.html', {'techniciens': techniciens})

def technicien_create(request):
    if request.method == 'POST':
        form = TechnicienForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('technicien_list')
    else:
        form = TechnicienForm()
    return render(request, 'app_techniciens/technicien_form.html', {'form': form})

def technicien_update(request, pk):
    technicien = get_object_or_404(Technicien, pk=pk)
    if request.method == 'POST':
        form = TechnicienForm(request.POST, instance=technicien)
        if form.is_valid():
            form.save()
            return redirect('technicien_list')
    else:
        form = TechnicienForm(instance=technicien)
    return render(request, 'app_techniciens/technicien_form.html', {'form': form})

def technicien_delete(request, pk):
    technicien = get_object_or_404(Technicien, pk=pk)
    if request.method == 'POST':
        technicien.delete()
        return redirect('technicien_list')
    return render(request, 'app_techniciens/technicien_confirm_delete.html', {'technicien': technicien})
