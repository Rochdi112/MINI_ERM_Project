from django.urls import path
from . import views

urlpatterns = [
    path('', views.materiel_list, name='materiel_list'),
    path('create/', views.materiel_create, name='materiel_create'),
    path('<int:pk>/edit/', views.materiel_update, name='materiel_update'),
    path('<int:pk>/delete/', views.materiel_delete, name='materiel_delete'),
]
