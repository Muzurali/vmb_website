from django.db import models

class Partner(models.Model):
    name = models.CharField("Firma adı", max_length=100)
    logo = models.ImageField("Logo", upload_to="partners/")
    website = models.URLField("Web sitesi", blank=True)
    description = models.TextField("Kısa açıklama", blank=True)  # 👈 EKLE
    is_active = models.BooleanField("Aktif", default=True)
    order = models.PositiveIntegerField("Sıra", default=0)

    class Meta:
        ordering = ["order", "id"]

    def __str__(self):
        return self.name
