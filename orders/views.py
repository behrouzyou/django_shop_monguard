import datetime

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.conf import settings
from django.contrib import messages

from accounts.models import User
from .forms import *
import requests
import json

from products.models import Product
from .cart import Cart
from .forms import CartAddForm
from .models import *


class CartView(View):
    def get(self,request):
        cart=Cart(request)
        return render(request,'orders/cart.html',{'cart':cart})

class CartAddView(View):
    def post(self,request,product_id):
        cart=Cart(request)
        product =get_object_or_404(Product,id=product_id)
        form=CartAddForm(request.POST)
        if form.is_valid():
            cart.add(product,form.cleaned_data['quantity'])
        return redirect('orders:cart')
class CartRemoveView(View):
    def post(self,request,product_id):
        cart=Cart(request)
        product=get_object_or_404(Product,id=product_id)
        cart.remove(product)
        return redirect('orders:cart')

class OrderDetailView(LoginRequiredMixin,View):
    form_class =CouponApplyForm
    def get(self,request,order_id):
        order =get_object_or_404(Order,id=order_id)
        return render(request,'orders/order.html',{'order':order,'form':self.form_class})
class OrderCreateView(View):
    def get(self,request):
        cart=Cart(request)
        order=Order.objects.create(user=request.user)
        for item in cart:
            OrderItem.objects.create(order=order,product=item['product'],price=item['price'],quantity=item['quantity'])
            cart.clear()
            return redirect('orders:order_detail',order.id)

class OrderPayView(LoginRequiredMixin, View):
    def get(self, request, order_id):
        order = get_object_or_404(Order, id=order_id)
        request.session["order_pay"] = {"order_id":order.id}
        zp_req_headers = {'accept': 'application/json', 'content-type': 'application/json'}
        zp_req_data = {"merchant_id":settings.ZP_MERCHANT_ID,
                       "amount":order.get_total_price(),
                       "description":f"{order.user} - {order.updated}",
                       "metadata":{"mobile":f"{request.user.phone_number}", "email":f"{request.user.email}"},
                       "callback_url":"https://example.ir/orders/verify/"}
        zp_req = requests.post(settings.ZP_API_REQUEST, data=json.dumps(zp_req_data), headers=zp_req_headers)

        if zp_req.json()["data"]["code"] == 100:
            zp_authority = zp_req.json()["data"]["authority"]
            return redirect(f"https://payment.zarinpal.com/pg/StartPay/{zp_authority}")
        else:
            messages.error(request, "Error, transaction aborted or something else is wrong..!", "danger")
            return redirect("home:home")
class OrderVerifyView(LoginRequiredMixin, View):
    def get(self, request):
        order_id = request.session['order_pay']['order_id']
        order = get_object_or_404(Order, id=order_id)
        zp_authority = request.GET.get("Authority")
        zp_status = request.GET.get("Status")
        if zp_status == "OK":
            zp_req_headers = {'accept': 'application/json', 'content-type': 'application/json'}
            zp_req_data = {"merchant_id": settings.ZP_MERCHANT_ID,"amount": order.get_total_price(), "authority":zp_authority}
            zp_verity_req = requests.post(settings.ZP_API_VERIFY, data=json.dumps(zp_req_data), headers=zp_req_headers)

            if len(zp_verity_req.json()["error"]) == 0 and zp_verity_req.json()["data"]["code"] == 100:
                order.paid = True
                order.save()
                messages.success(request, "you paid successfully", "success")
                return redirect("home:home")
            else:
                zp_error_code = zp_verity_req.json()["errors"]["code"]
                zp_error_message = zp_verity_req.json()["errors"]["message"]
                messages.error(request, f"Error {zp_error_code}, {zp_error_message}..!", "danger")
                return redirect("home:home")
        else:
            messages.error(request, "Error, transaction aborted or something else is wrong..!", "danger")
            return redirect("home:home")
class CouponApplyView(LoginRequiredMixin,View):
    form_class=CouponApplyForm
    def post(self,request,order_id):
        now= datetime.datetime.now()
        form=self.form_class(request.POST)
        if form.is_valid():
            code=form.cleaned_data['code']
            try:
                coupon=Coupon.objects.get(code__exact=code,valid_from__lte=now,valid_to__gte=now,active=True)
            except Coupon.DoesNotExist:
                messages.success(request,'code doesnot exists','danger')
                return redirect('orders:order_detail',order_id)
            order=Order.objects.get(id=order_id)
            order.discount=coupon.discount
            order.save()
            return redirect('orders:order_detail',order_id)