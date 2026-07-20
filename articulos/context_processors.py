from django.conf import settings
from .models import Categoria


def site_settings(request):
    return {
        "categorias_nav": Categoria.objects.all(),
        "SITE_NAME": settings.SITE_NAME,
        "SITE_DESCRIPTION": settings.SITE_DESCRIPTION,
        "ADSENSE_CLIENT_ID": settings.ADSENSE_CLIENT_ID,
        "ADSENSE_SLOT_HEADER": settings.ADSENSE_SLOT_HEADER,
        "ADSENSE_SLOT_INARTICLE": settings.ADSENSE_SLOT_INARTICLE,
        "ADSENSE_SLOT_SIDEBAR": settings.ADSENSE_SLOT_SIDEBAR,
        "GOOGLE_ANALYTICS_ID": settings.GOOGLE_ANALYTICS_ID,
    }
