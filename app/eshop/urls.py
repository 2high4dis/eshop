from django.urls import path
from eshop.views import index, product_grid, product_page, shopping_cart, add_item_to_cart, add_item_to_favourites, \
    favourites, delete_from_cart, create_review, delete_review, order_view, shipping_info_choice, create_shipping_info, \
    add_shipping_info_to_order, delete_order, update_shipping_info, delete_shipping_info, payment, send_order, complete_order

urlpatterns = [
    path('', index, name='index'),
    path('catalog/<int:page_number>', product_grid, name='catalog'),
    path('catalog/product/<int:product_id>/',
         product_page, name='product_page'),
    path('cart/', shopping_cart, name='cart'),
    path('catalog/product/<int:product_id>/add/',
         add_item_to_cart, name='add_item_to_cart'),
    path('catalog/products/<int:product_id>/favourites/',
         add_item_to_favourites, name='add_item_to_favourites'),
    path('favourites/', favourites, name='favourites'),
    path('cart/<int:item_id>/delete/', delete_from_cart, name='delete_from_cart'),
    path('catalog/product/<int:product_id>/create_review',
         create_review, name='create_review'),
    path('review/<int:review_id>/delete', delete_review, name='delete_review'),
    path('profile/orders/<int:order_id>/', order_view, name='order_view'),
    path('orders/<int:order_id>/shipping/', shipping_info_choice,
         name='shipping_info_choice'),
    path('profile/shipping_info/add',
         create_shipping_info, name='create_shipping_info'),
    path('orders/<int:order_id>/shipping/submit',
         add_shipping_info_to_order, name='add_shipping_info_to_order'),
    path('order/<int:order_id>/delete', delete_order, name='delete_order'),
    path('profile/shipping_info/<int:info_id>/update',
         update_shipping_info, name='update_shipping_info'),
    path('profle/shipping_info/<int:info_id>/delete',
         delete_shipping_info, name='delete_shipping_info'),
    path('orders/<int:order_id>/payment', payment, name='payment'),
    path('orders/<int:order_id>/send', send_order, name='send_order'),
    path('orders/<int:order_id>/complete',
         complete_order, name='complete_order')
]
