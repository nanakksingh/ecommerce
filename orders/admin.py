from django.contrib import admin
from .models import Order, OrderItem
# Register your models here.

class OrderItemInline(admin.TabularInline):
	model = OrderItem
	raw_id_fields = ['product']

class OrderAdmin(admin.ModelAdmin):
	list_display = ['id', 'first_name', 'last_name', 'email', 'address', 'postal_code', 'city',
								'paid', 'created', 'updated']
	list_filter = ['paid', 'created', 'updated']
	inlines = [OrderItemInline]

# 	def order_pdf(obj):
# 		return '<a href="{}">PDF</a>'.format(reverse('orders:admin_order_pdf', args=[obj.id]))
# 	order_pdf.allow_tags = True
# 	order_pdf.short_description = 'PDF bill'
admin.site.register(Order, OrderAdmin)									