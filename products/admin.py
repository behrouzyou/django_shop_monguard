from django.contrib import admin

from products.models import Category, Product

admin.site.register(Category)
@admin.register(Product)
class AdminProduct(admin.ModelAdmin):
    list_display = ('name','price','created')
    search_fields = ('name','price','category')
    raw_id_fields = ('category',)
