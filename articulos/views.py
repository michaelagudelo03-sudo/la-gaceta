from django.core.paginator import Paginator
from django.db.models import F, Q
from django.shortcuts import render, get_object_or_404
from django.utils import timezone

from .models import Articulo, Categoria


def _publicados():
    return Articulo.objects.filter(estado=Articulo.Estado.PUBLICADO, fecha_publicacion__lte=timezone.now())


def portada(request):
    base = _publicados().select_related("categoria", "autor")
    destacado = base.filter(destacado=True).first()
    lista = base.exclude(pk=destacado.pk) if destacado else base
    paginator = Paginator(lista, 9)
    pagina = paginator.get_page(request.GET.get("pagina"))
    categorias = Categoria.objects.all()
    return render(request, "articulos/portada.html", {
        "destacado": destacado,
        "pagina": pagina,
        "categorias": categorias,
    })


def detalle(request, slug):
    articulo = get_object_or_404(_publicados().select_related("categoria", "autor"), slug=slug)
    Articulo.objects.filter(pk=articulo.pk).update(vistas=F("vistas") + 1)
    relacionados = _publicados().filter(categoria=articulo.categoria).exclude(pk=articulo.pk)[:3]
    return render(request, "articulos/detalle.html", {
        "articulo": articulo,
        "relacionados": relacionados,
    })


def categoria(request, slug):
    cat = get_object_or_404(Categoria, slug=slug)
    lista = _publicados().filter(categoria=cat).select_related("categoria", "autor")
    paginator = Paginator(lista, 9)
    pagina = paginator.get_page(request.GET.get("pagina"))
    return render(request, "articulos/categoria.html", {"categoria": cat, "pagina": pagina})


def buscar(request):
    q = request.GET.get("q", "").strip()
    resultados = _publicados().filter(Q(titulo__icontains=q) | Q(resumen__icontains=q) | Q(contenido__icontains=q)) if q else []
    return render(request, "articulos/buscar.html", {"q": q, "resultados": resultados})
