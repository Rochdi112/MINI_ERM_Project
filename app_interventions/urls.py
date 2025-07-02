from django.urls import path
from . import views

urlpatterns = [
    path('', views.intervention_list, name='intervention_list'),
    path('create/', views.intervention_create, name='intervention_create'),
    path('<int:pk>/edit/', views.intervention_update, name='intervention_update'),
    path('<int:pk>/delete/', views.intervention_delete, name='intervention_delete'),
]
