from django.contrib.sitemaps import Sitemap
from .models import Articulo


class ArticuloSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8

    def items(self):
        return Articulo.objects.filter(estado=Articulo.Estado.PUBLICADO)

    def lastmod(self, obj):
        return obj.actualizado
