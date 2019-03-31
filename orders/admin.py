from django.contrib import admin
from .models import Order, OrderItem, Pay


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['order','product']


class OrderAdmin(admin.ModelAdmin):
    list_display = ['id','user', 'paid', 'created',
                    'updated']
    list_filter = ['paid', 'created', 'updated']
    inlines = [OrderItemInline]


admin.site.register(Order, OrderAdmin)
admin.site.register(Pay)
