from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail
from django.http import Http404
from django.shortcuts import redirect, render

from .content import SERVICES, SERVICE_DETAILS
from .forms import ContactForm , QuoteForm
from django.core.mail import EmailMessage




def home(request):
    return render(request, "core/home.html", {"services": SERVICES})


def services(request):
    return render(request, "core/services.html", {"services": SERVICES})


def service_detail(request, slug):
    svc = next((s for s in SERVICES if s["slug"] == slug), None)
    if not svc:
        raise Http404("Hizmet bulunamadı")

    detail = SERVICE_DETAILS.get(slug)
    other_services = [s for s in SERVICES if s["slug"] != slug][:6]

    return render(
        request,
        "core/service_detail.html",
        {"service": svc, "detail": detail, "other_services": other_services},
    )

def about(request):
    return render(request, "core/about.html")



def contact(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            d = form.cleaned_data

            # Hizmetler (checkbox) -> okunabilir metin
            services_labels = []
            if d.get("services"):
                choices = dict(form.fields["services"].choices)
                services_labels = [choices.get(k, k) for k in d["services"]]

            subject = (d.get("subject") or "").strip() or "İletişim / Teklif Talebi"

            body_lines = [
                f"Ad Soyad: {d.get('name','')}",
                f"E-posta: {d.get('email','')}",
                f"Telefon: {d.get('phone','')}",
            ]

            # Teklif alanları doluysa ekle
            if d.get("company"):
                body_lines.append(f"Firma Ünvanı: {d.get('company')}")

            if services_labels:
                body_lines.append(f"Hizmetler: {', '.join(services_labels)}")

            if d.get("monthly_count") is not None:
                body_lines.append(f"Aylık belge/adet: {d.get('monthly_count')}")

            body_lines.append("")  # boş satır
            body_lines.append("Mesaj:")
            body_lines.append(d.get("message", ""))

            body = "\n".join(body_lines)

            send_mail(
                subject=f"[VM Bilgisayar] {subject}",
                message=body,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.CONTACT_TO_EMAIL],
                fail_silently=False,
            )

            messages.success(request, "Mesajınız alındı. En kısa sürede dönüş yapacağız.")
            return redirect("contact")

        messages.error(request, "Formda hata var. Lütfen alanları kontrol edin.")
    else:
        form = ContactForm()

    return render(request, "core/contact.html", {"form": form})

def quote(request):
    print("QUOTE METHOD:", request.method)
    if request.method == "POST":
        form = QuoteForm(request.POST)
        print("POST DATA:", request.POST)
        print("FORM ERRORS:", form.errors)
        if form.is_valid():
            d = form.cleaned_data

            services_labels = []
            if d.get("services"):
                choices = dict(form.fields["services"].choices)
                services_labels = [choices.get(k, k) for k in d["services"]]

            subject = "Teklif Talebi"

            body_lines = [
                f"Teklif Tipi: {d.get('offer_type','')}",
                f"Ad Soyad: {d.get('name','')}",
                f"E-posta: {d.get('email','')}",
                f"Telefon: {d.get('phone','')}",
                f"Firma Ünvanı: {d.get('company','')}",
                f"VKN/TCKN: {d.get('tax_no','')}",
                f"ERP/Muhasebe: {d.get('erp_name','')}",
                f"Nereden Duydu: {d.get('heard_from','')}",
                f"e-Belge Kullanımı: {d.get('e_doc_usage','')}",
            ]

            if services_labels:
                body_lines.append(f"Hizmetler: {', '.join(services_labels)}")

            if d.get("monthly_count") is not None:
                body_lines.append(f"Aylık belge/adet: {d.get('monthly_count')}")

            body_lines.append("")
            body_lines.append("Not / Açıklama:")
            body_lines.append(d.get("message", "") or "-")

            body_lines.append("")
            body_lines.append(f"KVKK Onay: {d.get('consent')}")
            body_lines.append(f"Ticari İleti: {d.get('marketing_ok')}")

            body = "\n".join(body_lines)

            send_mail(
                subject=f"[VM Bilgisayar] {subject}",
                message=body,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.CONTACT_TO_EMAIL],
                fail_silently=False,
            )

            messages.success(request, "Teklif talebiniz alındı. En kısa sürede dönüş yapacağız.")
            return redirect("quote")

        messages.error(request, "Formda hata var. Lütfen alanları kontrol edin.")
    else:
        form = QuoteForm()

    return render(request, "core/quote.html", {"form": form})



