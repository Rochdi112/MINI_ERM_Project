from django.shortcuts import render, redirect, get_object_or_404
from .models import Intervention
from .forms import InterventionForm

def intervention_list(request):
    interventions = Intervention.objects.all()
    return render(request, 'app_interventions/intervention_list.html', {'interventions': interventions})

def intervention_create(request):
    if request.method == 'POST':
        form = InterventionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('intervention_list')
    else:
        form = InterventionForm()
    return render(request, 'app_interventions/intervention_form.html', {'form': form})

def intervention_update(request, pk):
    intervention = get_object_or_404(Intervention, pk=pk)
    if request.method == 'POST':
        form = InterventionForm(request.POST, instance=intervention)
        if form.is_valid():
            form.save()
            return redirect('intervention_list')
    else:
        form = InterventionForm(instance=intervention)
    return render(request, 'app_interventions/intervention_form.html', {'form': form})

def intervention_delete(request, pk):
    intervention = get_object_or_404(Intervention, pk=pk)
    if request.method == 'POST':
        intervention.delete()
        return redirect('intervention_list')
    return render(request, 'app_interventions/intervention_confirm_delete.html', {'intervention': intervention})
