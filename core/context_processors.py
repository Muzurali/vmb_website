from .content import SERVICES, CONTACT

def global_nav(request):
    return {
        "services_nav": SERVICES,
        "contact": CONTACT,
    }
