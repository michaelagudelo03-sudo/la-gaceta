# La Gaceta — plataforma de artículos con monetización

Sitio en Django para publicar artículos desde un panel de administración y
monetizarlos con Google AdSense. Incluye SEO básico (sitemap, meta tags,
`robots.txt`), categorías, buscador y diseño propio (no es una plantilla
genérica).

## 1. Ejecutarlo en tu computador

```bash
python3 -m venv venv
source venv/bin/activate          # en Windows: venv\Scripts\activate
pip install -r requirements.txt

cp .env.example .env              # y completa los valores (con DEBUG=True para desarrollo)

python manage.py migrate
python manage.py createsuperuser  # crea tu usuario para el panel
python manage.py runserver
```

Abre `http://127.0.0.1:8000/` para el sitio público y
`http://127.0.0.1:8000/admin/` para publicar artículos.

## 2. Publicar contenido

Todo se gestiona desde `/admin/`, sin necesidad de tocar código:

1. Crea **Categorías** (ej. Tecnología, Cultura, Mundo).
2. Crea un **Artículo**: título, resumen (para SEO y tarjetas), contenido
   (admite HTML: `<p>`, `<h2>`, `<img>`, `<blockquote>`, etc.), imagen de
   portada y categoría.
3. Cambia el **estado** a "Publicado" y define la fecha de publicación.
4. Marca **"Destacado"** en un solo artículo para que aparezca grande en
   portada con el sello de categoría.
5. Desmarca **"Permite anuncios"** si un artículo no debe mostrar publicidad.

## 3. Activar Google AdSense

1. Sube el sitio a un dominio propio con contenido real (AdSense exige
   dominio verificado y contenido original — no aprueba `localhost`).
2. Solicita tu cuenta en [google.com/adsense](https://www.google.com/adsense).
   Google revisa el sitio; el sitio ya sirve `ads.txt` y `robots.txt`, dos
   requisitos habituales de la revisión.
3. Cuando te aprueben, copia tu **Publisher ID** (`ca-pub-...`) y los
   **ID de bloque de anuncio** que crees en AdSense, y ponlos en `.env`:
   ```
   ADSENSE_CLIENT_ID=ca-pub-XXXXXXXXXXXXXXXX
   ADSENSE_SLOT_HEADER=xxxxxxxxxx
   ADSENSE_SLOT_INARTICLE=xxxxxxxxxx
   ADSENSE_SLOT_SIDEBAR=xxxxxxxxxx
   ```
4. También reemplaza el `pub-0000000000000000` real dentro de
   `blogmonetizado/urls.py` (función `ads_txt`) con tu Publisher ID.
5. Los anuncios aparecen solos: cabecera, dentro del artículo (antes y
   después del cuerpo) y barra lateral. Sin esos valores en `.env`, el sitio
   funciona igual pero sin espacios de anuncio.

**Nota realista:** AdSense suele tardar días o semanas en aprobar, y pide
tráfico y contenido genuino — no publiques artículos de relleno solo para
monetizar. Mientras tanto puedes lanzar el sitio y agregar los IDs después.

## 4. Poner el sitio en producción

Recomendado: **Railway** o **Render** (ambos tienen plan gratuito/económico
y soportan Django + PostgreSQL fácilmente).

Pasos generales:

1. Sube el proyecto a un repositorio de GitHub (el `.gitignore` ya excluye
   `.env` y `db.sqlite3`).
2. En Railway/Render, crea un servicio nuevo desde tu repo y añade una base
   de datos PostgreSQL (usa `dj-database-url` o define `DATABASE_URL` y
   ajusta `DATABASES` en `settings.py` — con SQLite los datos no persisten
   bien en estas plataformas).
3. Define las variables de entorno del `.env.example` en el panel del
   proveedor (con `DEBUG=False` y tu dominio real en `ALLOWED_HOSTS`).
4. El `Procfile` ya define cómo arrancar (`gunicorn`) y migrar
   automáticamente en cada despliegue.
5. Ejecuta `python manage.py collectstatic` (o dejar que el build lo haga)
   para que WhiteNoise sirva el CSS.
6. Conecta tu dominio propio desde el panel del proveedor.

## 5. Estructura del proyecto

```
blogmonetizado/     # configuración del proyecto (settings, urls)
articulos/          # la app: modelos, vistas, admin, sitemap
templates/           # HTML (base.html + plantillas de articulos/)
static/css/styles.css # diseño (paleta, tipografía, layout)
requirements.txt
Procfile
.env.example
```

## Próximos pasos sugeridos

- Suscripciones o contenido de pago: se puede añadir después con Stripe
  (paywall por artículo o membresía), si más adelante quieres combinar
  anuncios con pagos.
- Comentarios: se puede integrar Disqus o un sistema propio.
- Newsletter: capturar correos para enviar los nuevos artículos.
