from django.shortcuts import render
from .models import OrderItem
from .forms import OrderCreateForm
from cart.cart import Cart
# from .tasks import order_created
from django.conf import settings
from django.http import HttpResponse
from django.template.loader import render_to_string
from shop.models import Product
from shop.recommender import Recommender
# import weasyprint

# Create your views here.
def order_create(request):
	cart = Cart(request)
	if request.method == 'POST':
		form = OrderCreateForm(request.POST)
		if form.is_valid():
			order = form.save(commit = False)
			if cart.coupon:
				order.coupon = cart.coupon
				order.discount = cart.coupon.discount
			order.save()
			ptr = []	
			for item in cart:
				OrderItem.objects.create(order=order,
										 product = item['product'],
										 price = item['price'],
										 quantity = item['quantity'])
				ptr.append(Product.objects.get(name = item['product'].name))
			r = Recommender()
			r.products_bought(ptr)				
			cart.clear()
			request.session['coupon_id'] = None
			# order_created.delay(order.id)
			return render(request, 'orders/order/created.html', {'order':order})
	else:
		form = OrderCreateForm()
		return render(request, 'orders/order/create.html', {'cart':cart, 'form':form})			

# @staff_member_required
# def admin_order_pdf(request, order_id):
# 	order = get_object_or_404(Order, id = order_id)
# 	html = render_to_string('orders/order/pdf.html', {'order':order})

# 	response = HttpResponse(content_type = 'application/pdf')
# 	response['Content-Disposition'] = 'filename="order_{}.pdf"'.format(order.id)
# 	weasyprint.HTML(string=html).write_pdf(response, stylesheets=[weasyprint.CSS(settings.STATIC_ROOT + 'css/pdf.css')])
# 	return response		