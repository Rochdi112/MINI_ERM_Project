from django.urls import path
from .views import (
    ClientListView,
    ClientCreateView,
    ClientUpdateView,
    ClientDeleteView,
    SiteListView,
    SiteCreateView,
    SiteUpdateView,
    SiteDeleteView,
)

app_name = 'app_clients'

urlpatterns = [
    path('', ClientListView.as_view(), name='client_list'),
    path('create/', ClientCreateView.as_view(), name='client_create'),
    path('<int:pk>/edit/', ClientUpdateView.as_view(), name='client_update'),
    path('<int:pk>/delete/', ClientDeleteView.as_view(), name='client_delete'),
    path('sites/', SiteListView.as_view(), name='site_list'),
    path('sites/create/', SiteCreateView.as_view(), name='site_create'),
    path('sites/<int:pk>/edit/', SiteUpdateView.as_view(), name='site_update'),
    path('sites/<int:pk>/delete/', SiteDeleteView.as_view(), name='site_delete'),
]
