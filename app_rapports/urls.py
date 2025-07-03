from django.urls import path
from .views import (
    RapportListView,
    RapportCreateView,
    RapportUpdateView,
    RapportDeleteView,
    rapport_pdf,
    generate_pdf,
)

app_name = 'app_rapports'

urlpatterns = [
    path('', RapportListView.as_view(), name='rapport_list'),
    path('create/', RapportCreateView.as_view(), name='rapport_create'),
    path('<int:pk>/edit/', RapportUpdateView.as_view(), name='rapport_update'),
    path('<int:pk>/delete/', RapportDeleteView.as_view(), name='rapport_delete'),
    path('<int:pk>/pdf/', rapport_pdf, name='rapport_pdf'),
    path('<int:pk>/generate-pdf/', generate_pdf, name='generate_pdf'),
]
