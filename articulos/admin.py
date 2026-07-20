from django.contrib import admin
from .models import Articulo, Categoria


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ("nombre", "slug")
    prepopulated_fields = {"slug": ("nombre",)}
    search_fields = ("nombre",)


@admin.register(Articulo)
class ArticuloAdmin(admin.ModelAdmin):
    list_display = ("titulo", "autor", "categoria", "estado", "destacado", "fecha_publicacion", "vistas")
    list_filter = ("estado", "categoria", "destacado", "permite_anuncios")
    search_fields = ("titulo", "resumen", "contenido")
    prepopulated_fields = {"slug": ("titulo",)}
    date_hierarchy = "fecha_publicacion"
    readonly_fields = ("vistas", "creado", "actualizado")
    fieldsets = (
        ("Contenido", {"fields": ("titulo", "slug", "categoria", "resumen", "contenido", "imagen_portada")}),
        ("Publicación", {"fields": ("estado", "fecha_publicacion", "destacado", "autor")}),
        ("Monetización", {"fields": ("permite_anuncios",)}),
        ("Estadísticas", {"fields": ("vistas", "creado", "actualizado")}),
    )

    def save_model(self, request, obj, form, change):
        if not obj.pk and not obj.autor_id:
            obj.autor = request.user
        super().save_model(request, obj, form, change)


admin.site.site_header = "Panel de contenido"
admin.site.site_title = "Panel de contenido"
admin.site.index_title = "Gestión de artículos"
