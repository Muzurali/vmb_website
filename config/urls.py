from django.contrib import admin
from django.urls import path
from core import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.home, name="home"),
    path("hizmetler/", views.services, name="services"),
    path("hizmetler/<slug:slug>/", views.service_detail, name="service_detail"),
    path("hakkimizda/", views.about, name="about"),
    path("iletisim/", views.contact, name="contact"),
    path("teklif-al/", views.quote, name="quote"),

]

