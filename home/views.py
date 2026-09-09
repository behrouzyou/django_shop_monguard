from django.views import View
from django.shortcuts import render
import logging
from products.models import Product, Category

logger=logging.getLogger(__name__)

class HomeView(View):
    def get(self,request,category_slug=None):
        logger.info('Home activated')
        products = Product.objects.filter(available=True)
        categories = Category.objects.filter(is_sub=False)
        if category_slug:
            category =Category.objects.get(slug=category_slug)
            products =Product.objects.filter(category = category)
        return render(request,'home/index.html',{'products':products,'categories':categories})
