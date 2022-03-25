from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from cadastro.models import Conta

class ContaAdmin(UserAdmin):
    list_display = ('email', 'username', 'date_of_birth','date_joined', 'last_login',   'is_admin', 'is_staff')
    search_fields = ('email', 'username')
    readonly_fields = ('date_of_birth', 'date_joined', 'last_login')


    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


admin.site.register(Conta, ContaAdmin)