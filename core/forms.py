from django import forms
from .content import SERVICES


class ContactForm(forms.Form):
    # Honeypot (bot yakalama)
    website = forms.CharField(required=False, widget=forms.HiddenInput)

    name = forms.CharField(label="Ad Soyad", max_length=100)
    email = forms.EmailField(label="E-posta")
    phone = forms.CharField(label="Telefon", max_length=20, required=False)
    subject = forms.CharField(label="Konu", max_length=120, required=False)
    message = forms.CharField(label="Mesaj", widget=forms.Textarea(attrs={"rows": 4}))

    consent = forms.BooleanField(
        label="KVKK Onayı",
        required=True,
    )

    def clean_website(self):
        # Botlar bunu doldurur, insan boş bırakır
        v = self.cleaned_data.get("website", "")
        if v:
            raise forms.ValidationError("Bot tespit edildi.")
        return v


class QuoteForm(forms.Form):
    # SERVICES içinden seçenek üret
    SERVICE_CHOICES = []
    for s in SERVICES:
        label = s.get("title") or s.get("name") or s.get("label") or s.get("slug")
        SERVICE_CHOICES.append((s.get("slug"), label))

    services = forms.MultipleChoiceField(
        label="Hizmetler",
        choices=SERVICE_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        required=True,
    )

    name = forms.CharField(label="Ad Soyad", max_length=100, required=True)
    phone = forms.CharField(label="Telefon", max_length=20, required=True)
    email = forms.EmailField(label="E-posta", required=True)

    message = forms.CharField(
        label="Açıklama",
        widget=forms.Textarea(attrs={"rows": 4}),
        required=False,
    )
