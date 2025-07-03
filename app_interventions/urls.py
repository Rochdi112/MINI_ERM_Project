from django.urls import path
from .views import (
    InterventionListView,
    InterventionCreateView,
    InterventionUpdateView,
    InterventionDeleteView,
    checklist_view,
    upload_attachment,
    checklist_item_update,
    htmx_upload_attachment,
    htmx_checklist_toggle,
)
from . import views

app_name = 'app_interventions'

urlpatterns = [
    path('', InterventionListView.as_view(), name='intervention_list'),
    path('create/', InterventionCreateView.as_view(), name='intervention_create'),
    path('<int:pk>/edit/', InterventionUpdateView.as_view(), name='intervention_update'),
    path('<int:pk>/delete/', InterventionDeleteView.as_view(), name='intervention_delete'),
    path('<int:intervention_id>/checklist/', checklist_view, name='checklist'),
    path('<int:pk>/attachments/', upload_attachment, name='attachment_upload'),
    path('checklist/item/<int:pk>/edit/', checklist_item_update, name='checklist_item_update'),
    path('<int:pk>/htmx-upload/', htmx_upload_attachment, name='htmx_upload_attachment'),
    path('<int:pk>/htmx-checklist-item/', htmx_checklist_toggle, name='htmx_checklist_toggle'),
    path('<int:pk>/htmx-checklist-item/', views.toggle_checklist_item_htmx, name='htmx-checklist-item'),
    path('htmx-filter/', views.filter_interventions_htmx, name='htmx-filter'),
    path('htmx-modal-form/', views.modal_form_intervention_htmx, name='htmx-modal-form'),
]
