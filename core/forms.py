from django import forms

SERVICE_CHOICES = (
    ("e_fatura", "e-Fatura"),
    ("e_arsiv", "e-Arşiv"),
    ("e_irsaliye", "e-İrsaliye"),
    ("e_defter", "e-Defter"),
    ("entegrasyon", "Yazılım / Entegrasyon"),
    ("teknik_destek", "Bilgisayar / Teknik Destek"),
    ("diger", "Diğer"),
)

class ContactForm(forms.Form):
    name = forms.CharField(label="Ad Soyad", max_length=80)
    email = forms.EmailField(label="E-posta")
    phone = forms.CharField(label="Telefon", max_length=30, required=False)
    subject = forms.CharField(label="Konu", max_length=120, required=False)
    message = forms.CharField(label="Mesaj", widget=forms.Textarea)

    consent = forms.BooleanField(
        label="KVKK kapsamında benimle iletişime geçilmesini kabul ediyorum.",
        required=True
    )

    website = forms.CharField(required=False, widget=forms.HiddenInput)

    def clean_website(self):
        if self.cleaned_data.get("website"):
            raise forms.ValidationError("Spam tespit edildi.")
        return ""
OFFER_TYPE_CHOICES = [
    ("e_belge", "e-Belge Hizmetleri"),
    ("e_defter", "e-Defter"),
    ("on_muhasebe", "Ön Muhasebe"),
    ("mobil", "Mobil"),
    ("diger", "Diğer"),
]

HEARD_FROM_CHOICES = [
    ("sosyal", "Sosyal Medya"),
    ("google", "Google"),
    ("tavsiye", "Tavsiye"),
    ("bayi", "Bayi"),
    ("smmm", "SMMM / Mali Müşavir"),
    ("diger", "Diğer"),
]

E_DOC_USAGE_CHOICES = [
    ("yok", "Henüz kullanmıyorum"),
    ("gib", "GİB Portal"),
    ("entegrator", "Özel Entegratör"),
    ("direkt", "Direkt Entegrasyon"),
]

class QuoteForm(forms.Form):
    offer_type = forms.ChoiceField(
        label="Teklif Tipi",
        choices=OFFER_TYPE_CHOICES,
        widget=forms.Select(attrs={"class": "form-select"})
    )

    name = forms.CharField(
        label="Ad Soyad",
        max_length=80,
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Ad Soyad"})
    )

    email = forms.EmailField(
        label="E-posta",
        widget=forms.EmailInput(attrs={"class": "form-control", "placeholder": "ornek@firma.com"})
    )

    phone = forms.CharField(
        label="Telefon",
        max_length=30,
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "05xx xxx xx xx"})
    )

    company = forms.CharField(
        label="Firma Ünvanı",
        max_length=120,
        widget=forms.TextInput(attrs={"class": "form-control"})
    )

    tax_no = forms.CharField(
        label="VKN/TCKN",
        max_length=11,
        required=False,
        widget=forms.TextInput(attrs={"class": "form-control"})
    )

    erp_name = forms.CharField(
        label="ERP / Muhasebe Programı",
        max_length=120,
        required=False,
        widget=forms.TextInput(attrs={"class": "form-control"})
    )

    heard_from = forms.ChoiceField(
        label="Bizi nereden duydunuz?",
        choices=HEARD_FROM_CHOICES,
        required=False,
        widget=forms.Select(attrs={"class": "form-select"})
    )

    e_doc_usage = forms.ChoiceField(
        label="e-Belge kullanıyor musunuz?",
        choices=E_DOC_USAGE_CHOICES,
        required=False,
        widget=forms.Select(attrs={"class": "form-select"})
    )

    monthly_count = forms.IntegerField(
        label="Aylık ortalama belge/adet",
        required=False,
        min_value=0,
        widget=forms.NumberInput(attrs={"class": "form-control"})
    )

    services = forms.MultipleChoiceField(
        label="İlgilendiğiniz Hizmetler",
        choices=SERVICE_CHOICES,
        required=False,
        widget=forms.CheckboxSelectMultiple
    )

    message = forms.CharField(
        label="Not / Açıklama",
        required=False,
        widget=forms.Textarea(attrs={"class": "form-control", "rows": 4})
    )

    consent = forms.BooleanField(
        label="KVKK kapsamında benimle iletişime geçilmesini kabul ediyorum.",
        required=True,
        widget=forms.CheckboxInput(attrs={"class": "form-check-input"})
    )

    marketing_ok = forms.BooleanField(
        label="Ticari elektronik ileti almak istiyorum.",
        required=False,
        widget=forms.CheckboxInput(attrs={"class": "form-check-input"})
    )

    website = forms.CharField(required=False, widget=forms.HiddenInput)
