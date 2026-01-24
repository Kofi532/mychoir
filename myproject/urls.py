from django.contrib import admin
from django.urls import path, include # Make sure 'include' is imported
from django.contrib.sitemaps.views import sitemap
from .sitemaps import HymnSitemap

sitemaps = {
    'hymns': HymnSitemap,
}


urlpatterns = [
    path('admin/', admin.site.urls),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    path('', include('choir.urls')), # This tells Django to check choir/urls.py
]