from django.urls import path
from .views import (
    TechnicienListView,
    TechnicienCreateView,
    TechnicienUpdateView,
    TechnicienDeleteView,
)

app_name = 'app_techniciens'

urlpatterns = [
    path('', TechnicienListView.as_view(), name='technicien_list'),
    path('create/', TechnicienCreateView.as_view(), name='technicien_create'),
    path('<int:pk>/edit/', TechnicienUpdateView.as_view(), name='technicien_update'),
    path('<int:pk>/delete/', TechnicienDeleteView.as_view(), name='technicien_delete'),
]
