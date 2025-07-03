from django.urls import path
from . import views

app_name = 'app_techniciens'

urlpatterns = [
    path('', views.technicien_list, name='technicien_list'),
    path('create/', views.technicien_create, name='technicien_create'),
    path('<int:pk>/edit/', views.technicien_update, name='technicien_update'),
    path('<int:pk>/delete/', views.technicien_delete, name='technicien_delete'),
]
