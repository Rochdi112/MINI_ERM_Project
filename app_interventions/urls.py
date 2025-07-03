from django.urls import path
from . import views

app_name = 'app_interventions'

urlpatterns = [
    path('', views.intervention_list, name='intervention_list'),
    path('create/', views.intervention_create, name='intervention_create'),
    path('<int:pk>/edit/', views.intervention_update, name='intervention_update'),
    path('<int:pk>/delete/', views.intervention_delete, name='intervention_delete'),
    path('<int:intervention_id>/checklist/', views.checklist_view, name='checklist'),
    path('<int:intervention_id>/attachments/', views.attachment_upload, name='attachment_upload'),
    path('checklist/item/<int:pk>/edit/', views.checklist_item_update, name='checklist_item_update'),
    path('<int:pk>/htmx-upload/', views.htmx_upload_attachment, name='htmx_upload_attachment'),
]
