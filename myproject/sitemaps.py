import json
import os
from django.conf import settings
from django.contrib.sitemaps import Sitemap
from django.urls import reverse

class HymnSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8

    def items(self):
        # Load your JSON data
        json_path = os.path.join(settings.BASE_DIR, 'static', 'sample.json')
        with open(json_path, 'r') as f:
            hymns = json.load(f)
        return [hymn['title'] for hymn in hymns]

    def location(self, item):
        # Generates: /?hymn=mhb105
        return f"/?hymn={item}"