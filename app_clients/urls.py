from django.urls import path
from .views import (
    ClientListView,
    ClientCreateView,
    ClientUpdateView,
    ClientDeleteView,
)

app_name = 'app_clients'

urlpatterns = [
    path('', ClientListView.as_view(), name='client_list'),
    path('create/', ClientCreateView.as_view(), name='client_create'),
    path('<int:pk>/edit/', ClientUpdateView.as_view(), name='client_update'),
    path('<int:pk>/delete/', ClientDeleteView.as_view(), name='client_delete'),
]
