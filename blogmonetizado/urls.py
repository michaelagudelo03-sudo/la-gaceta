from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.http import HttpResponse
from django.urls import path, include

from articulos.sitemaps import ArticuloSitemap

sitemaps = {"articulos": ArticuloSitemap}


def robots_txt(request):
    contenido = "User-agent: *\nAllow: /\nSitemap: /sitemap.xml\n"
    return HttpResponse(contenido, content_type="text/plain")


def ads_txt(request):
    # Reemplaza pub-0000000000000000 por tu ID real cuando AdSense te lo entregue.
    contenido = "google.com, pub-0000000000000000, DIRECT, f08c47fec0942fa0\n"
    return HttpResponse(contenido, content_type="text/plain")


urlpatterns = [
    path("admin/", admin.site.urls),
    path("sitemap.xml", sitemap, {"sitemaps": sitemaps}, name="sitemap"),
    path("robots.txt", robots_txt),
    path("ads.txt", ads_txt),
    path("", include("articulos.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
