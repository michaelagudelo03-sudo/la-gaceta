from django.db import models
from django.conf import settings
from django.urls import reverse
from django.utils.text import slugify
from django.utils import timezone


class Categoria(models.Model):
    nombre = models.CharField(max_length=80, unique=True)
    slug = models.SlugField(max_length=90, unique=True, blank=True)
    descripcion = models.CharField(max_length=200, blank=True)

    class Meta:
        verbose_name = "categoría"
        verbose_name_plural = "categorías"
        ordering = ["nombre"]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nombre)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nombre

    def get_absolute_url(self):
        return reverse("articulos:categoria", args=[self.slug])


class Articulo(models.Model):
    class Estado(models.TextChoices):
        BORRADOR = "borrador", "Borrador"
        PUBLICADO = "publicado", "Publicado"

    titulo = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True, blank=True)
    autor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name="articulos")
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True, blank=True, related_name="articulos")
    resumen = models.CharField(max_length=280, help_text="Aparece en las tarjetas de listado y como meta descripción.")
    contenido = models.TextField(help_text="Admite HTML básico (párrafos, negritas, enlaces, imágenes).")
    imagen_portada = models.ImageField(upload_to="portadas/%Y/%m/", blank=True, null=True)
    estado = models.CharField(max_length=10, choices=Estado.choices, default=Estado.BORRADOR)
    destacado = models.BooleanField(default=False, help_text="Se muestra en la cabecera de portada.")
    permite_anuncios = models.BooleanField(default=True, help_text="Desactívalo para artículos sin publicidad (ej. patrocinados aparte).")
    fecha_publicacion = models.DateTimeField(default=timezone.now)
    creado = models.DateTimeField(auto_now_add=True)
    actualizado = models.DateTimeField(auto_now=True)
    vistas = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["-fecha_publicacion"]

    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify(self.titulo)[:200]
            slug = base
            i = 1
            while Articulo.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                i += 1
                slug = f"{base}-{i}"
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.titulo

    def get_absolute_url(self):
        return reverse("articulos:detalle", args=[self.slug])

    @property
    def esta_publicado(self):
        return self.estado == self.Estado.PUBLICADO and self.fecha_publicacion <= timezone.now()
