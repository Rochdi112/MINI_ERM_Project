from django.urls import path
from .views import (
    MaterielListView,
    MaterielCreateView,
    MaterielUpdateView,
    MaterielDeleteView,
)

app_name = 'app_materiels'

urlpatterns = [
    path('', MaterielListView.as_view(), name='materiel_list'),
    path('create/', MaterielCreateView.as_view(), name='materiel_create'),
    path('<int:pk>/edit/', MaterielUpdateView.as_view(), name='materiel_update'),
    path('<int:pk>/delete/', MaterielDeleteView.as_view(), name='materiel_delete'),
]
