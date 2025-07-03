from django.urls import path
from . import views

app_name = 'app_rapports'

urlpatterns = [
    path('', views.rapport_list, name='rapport_list'),
    path('create/', views.rapport_create, name='rapport_create'),
    path('<int:pk>/pdf/', views.rapport_pdf, name='rapport_pdf'),
]
