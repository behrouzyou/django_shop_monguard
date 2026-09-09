from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib import admin
from .models import *
from .forms import *
from django.shortcuts import redirect

class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    list_display = ('email','phone_number','is_admin')
    list_filter = ('is_admin',)
    fieldsets = [
        [None,{'fields':['email','phone_number','full_name','password']}],
        ['Permissions',{'fields':['is_active','is_admin','last_login','is_superuser','groups','user_permissions']}]
    ]
    add_fieldsets = [
        [None,{'fields':['phone_number','email','full_name','password1','password2']}]
    ]
    search_fields = ['email','full_name']
    ordering = ['full_name']
    filter_horizontal = ['groups','user_permissions']
    def get_form(self,request,obj,**kwargs):
        form=super().get_form(request,obj,**kwargs)
        is_superuser=request.user.is_superuser
        if not is_superuser:
            form.base_fields['is_superuser'].disabled=True
        return form

    def response_change(self, request, obj):
        if '_saveupper' in request.POST:
            obj.full_name = obj.full_name.upper()
            obj.save()
            self.message_user(request, 'object saved uppercase', 'success')
            return redirect('admin:accounts_user_changelist')
        return super().response_change(request, obj)



# @admin.register(Avatar)
# class AvatarAdmin(admin.ModelAdmin):
#     readonly_fields = ["avatar_pic"]
#
#     def avatar_pic(self, obj):
#         return mark_safe(f"<img src='{obj.picture.url}' width='{obj.picture.width}' />")

admin.site.register(User,UserAdmin)

@admin.register(OtpCode)
class OtpCodeAdmin(admin.ModelAdmin):
    list_display =('phone_number','code','created')
admin.site.register(Avatar)