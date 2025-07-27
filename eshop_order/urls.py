from django.urls import path

from eshop_order.views import add_new_order, cart, send_request, verify, remove_cart_item

app_name = 'eshop_products'

urlpatterns = [
    path('add-new-order', add_new_order),
    path('cart', cart),
    path('remove-cart-item/<detail_id>', remove_cart_item),
    path('request/', send_request, name='request'),
    path('verify/<order_id>', verify, name='verify'),
]