from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from app_aggregator.views import SessionsList

urlpatterns = [
    path('', SessionsList.as_view(), name='sessions_list'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
