from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail, EmailMessage
from django.http import Http404
from django.shortcuts import redirect, render

from .content import SERVICES, SERVICE_DETAILS
from .forms import ContactForm, QuoteForm
from .models import Partner


def home(request):
    partners = Partner.objects.filter(is_active=True).order_by("order")[:3]
    return render(
        request,
        "core/home.html",
        {
            "services": SERVICES,
            "partners": partners,
        },
    )


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

            if d.get("company"):
                body_lines.append(f"Firma Ünvanı: {d.get('company')}")

            if services_labels:
                body_lines.append(f"Hizmetler: {', '.join(services_labels)}")

            if d.get("monthly_count") is not None:
                body_lines.append(f"Aylık belge/adet: {d.get('monthly_count')}")

            body_lines.append("")
            body_lines.append("Mesaj:")
            body_lines.append(d.get("message", ""))

            body = "\n".join(body_lines)

            email = EmailMessage(
                subject=f"[VM Bilgisayar] {subject}",
                body=body,
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[settings.CONTACT_TO_EMAIL],
            )

            # reply_to sadece email varsa ekle (None göndermeyelim)
            if d.get("email"):
                email.reply_to = [d.get("email")]

            email.send(fail_silently=False)

            messages.success(request, "Mesajınız alındı. En kısa sürede dönüş yapacağız.")
            return redirect("contact")

        print("CONTACT FORM ERRORS:", form.errors)
        print("CONTACT FORM DATA:", request.POST)
        messages.error(request, "Formda hata var. Lütfen alanları kontrol edin.")
    else:
        form = ContactForm()

    return render(request, "core/contact.html", {"form": form})


def quote(request):
    if request.method == "POST":
        form = QuoteForm(request.POST)
        if form.is_valid():
            d = form.cleaned_data

            # checkbox slug -> label
            choices = dict(form.fields["services"].choices)
            services_labels = [choices.get(k, k) for k in d.get("services", [])]

            body_lines = [
                f"Ad Soyad: {d.get('name')}",
                f"Telefon: {d.get('phone')}",
                f"E-posta: {d.get('email')}",
                f"Hizmetler: {', '.join(services_labels)}",
                "",
                "Açıklama:",
                d.get("message") or "-",
            ]
            body = "\n".join(body_lines)

            send_mail(
                subject="[VM Bilgisayar] Teklif Talebi",
                message=body,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.CONTACT_TO_EMAIL],
                fail_silently=False,
            )

            messages.success(request, "Teklif talebiniz alındı. En kısa sürede dönüş yapacağız.")
            return redirect("quote")

        FIELD_LABELS = {
            "services": "Hizmetler",
            "name": "Ad Soyad",
            "phone": "Telefon",
            "email": "E-posta",
            "message": "Açıklama",
        }

        missing_fields = []
        for field in form.errors:
            missing_fields.append(FIELD_LABELS.get(field, field))

        msg = "Lütfen aşağıdaki alanları doldurun:\n- " + "\n- ".join(missing_fields)
        messages.error(request, msg)
    else:
        form = QuoteForm()

    return render(request, "core/quote.html", {"form": form})



