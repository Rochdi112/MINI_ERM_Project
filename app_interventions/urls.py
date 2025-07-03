from django.urls import path
from .views import (
    InterventionListView,
    InterventionCreateView,
    InterventionUpdateView,
    InterventionDeleteView,
)

app_name = 'app_interventions'

urlpatterns = [
    path('', InterventionListView.as_view(), name='intervention_list'),
    path('create/', InterventionCreateView.as_view(), name='intervention_create'),
    path('<int:pk>/edit/', InterventionUpdateView.as_view(), name='intervention_update'),
    path('<int:pk>/delete/', InterventionDeleteView.as_view(), name='intervention_delete'),
    path('<int:intervention_id>/checklist/', views.checklist_view, name='checklist'),
    path('<int:intervention_id>/attachments/', views.attachment_upload, name='attachment_upload'),
    path('checklist/item/<int:pk>/edit/', views.checklist_item_update, name='checklist_item_update'),
    path('<int:pk>/htmx-upload/', views.htmx_upload_attachment, name='htmx_upload_attachment'),
]
