from django.shortcuts import render, get_object_or_404
from django.views import View

from orders.forms import CartAddForm
from .models import Product,Category

class ProductDetailView(View):
    def get(self,request,slug):
        product =get_object_or_404(Product,slug=slug)
        form=CartAddForm()
        return render(request,'home/detail.html',{'product':product,'form':form})
