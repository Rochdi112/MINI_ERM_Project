from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),

    path('clients/', include('app_clients.urls')),
    path('techniciens/', include('app_techniciens.urls')),
    path('interventions/', include('app_interventions.urls')),
    path('materiels/', include('app_materiels.urls')),
    path('rapports/', include('app_rapports.urls')),
]

# Pour servir les fichiers media en dev
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
