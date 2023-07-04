from django.contrib import admin
from eshop.models import Category, SubCategory, Product, ItemImage, Review,\
    ReviewImage, Country, City, ShippingCompany, Department, ShippingInfo, Brand, \
    Size, Cart, Favourite, Order, OrderItem

admin.site.register(Category)
admin.site.register(SubCategory)
admin.site.register(Brand)
admin.site.register(Product)
admin.site.register(ItemImage)
admin.site.register(Review)
admin.site.register(ReviewImage)
admin.site.register(Country)
admin.site.register(City)
admin.site.register(ShippingCompany)
admin.site.register(Department)
admin.site.register(ShippingInfo)
admin.site.register(Size)
admin.site.register(Cart)
admin.site.register(Favourite)
admin.site.register(Order)
admin.site.register(OrderItem)
