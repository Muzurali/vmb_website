from django.contrib import admin
from django.urls import path
from core import views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),

    path("", views.home, name="home"),
    path("hizmetler/", views.services, name="services"),
    path("hizmetler/<slug:slug>/", views.service_detail, name="service_detail"),
    path("hakkimizda/", views.about, name="about"),
    path("iletisim/", views.contact, name="contact"),
    path("teklif-al/", views.quote, name="quote"),
]

# ✅ SADECE DEBUG MODE'DA STATIC & MEDIA SERVİS ET
if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )
    urlpatterns += static(
        settings.STATIC_URL,
        document_root=settings.STATIC_ROOT
    )
