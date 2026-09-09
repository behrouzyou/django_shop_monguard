from django.contrib.sitemaps import Sitemap
from .models import Product


class ProductSitemap(Sitemap):
    changefreq = "weekly"
    priority = 1
    # protocol = 'https'


    def items(self):
        return Product.objects.all()

    def lastmod(self, obj):
        return obj.updated
