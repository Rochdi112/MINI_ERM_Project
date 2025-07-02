from django.shortcuts import render, redirect, get_object_or_404
from .models import Rapport
from .forms import RapportForm
from django.http import HttpResponse
from django.template.loader import render_to_string
from weasyprint import HTML
import tempfile

def rapport_list(request):
    rapports = Rapport.objects.all()
    return render(request, 'app_rapports/rapport_list.html', {'rapports': rapports})

def rapport_create(request):
    if request.method == 'POST':
        form = RapportForm(request.POST)
        if form.is_valid():
            rapport = form.save()
            return redirect('rapport_list')
    else:
        form = RapportForm()
    return render(request, 'app_rapports/rapport_form.html', {'form': form})

def rapport_pdf(request, pk):
    rapport = get_object_or_404(Rapport, pk=pk)
    html_string = render_to_string('app_rapports/pdf_template.html', {'rapport': rapport})

    html = HTML(string=html_string)
    result = tempfile.NamedTemporaryFile(delete=True)
    html.write_pdf(target=result.name)

    with open(result.name, 'rb') as pdf:
        response = HttpResponse(pdf.read(), content_type='application/pdf')
        response['Content-Disposition'] = f'inline; filename=rapport_{rapport.id}.pdf'
        return response
