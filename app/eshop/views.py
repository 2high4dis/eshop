from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, Brand, SubCategory, Category, footwear_sizes, wear_sizes, Size, Cart, Favourite,\
    Review, ReviewImage, Order, ShippingInfo, City, ShippingCompany, Department, OrderItem
from django.http import HttpRequest
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.core.paginator import Paginator
from math import ceil
from django.contrib import messages
from django.core.mail import send_mail

categories = Category.objects.all()
brands = Brand.objects.all()

context = {
    'categories': categories,
    'brands': brands,
}

subjects = {
    'In cart': 'was created!',
    'Confirmed': 'was completed!',
    'Paid': 'was paid!',
    'Sent': 'was sent!',
    'Completed': 'was completed!',
}

body = '''
Hello, %s!

Order #%s %s
 
Thank you!
~ Leonid
'''


def index(request):
    template_name = r'eshop/index.html'

    products = Product.objects.all()[:15]

    products_pgs = [products[:5], products[5:10], products[10:]]

    context.update({
        'products_pgs': products_pgs
    })
    return render(request=request, template_name=template_name, context=context)


def product_grid(request: HttpRequest, page_number: int):
    template_name = r'eshop/product_grid.html'
    products = Product.objects.all()

    category = request.GET.get('category')
    brand = request.GET.get('brand')
    size = request.GET.get('size')
    subcategory = request.GET.get('subcategory')
    only_in_stock = bool(request.GET.get('only_in_stock'))
    q = request.GET.get('q')

    subcategories = SubCategory.objects.all()

    sizes = wear_sizes + footwear_sizes

    if category:
        subcategories = subcategories.filter(category__category_name=category)
        products = products.filter(category__category__category_name=category)
        if category == 'Footwear':
            sizes = footwear_sizes
        else:
            sizes = wear_sizes

    if only_in_stock:
        for product in products:
            if product.in_stock() <= 0:
                products = products.exclude(pk=product.id)

    if brand != "Brand" and brand:
        products = products.filter(brand__brand=brand)

    if size != "Size" and size:
        products = products.filter(size__size=size)

    if subcategory != "Category" and subcategory:
        products = products.filter(category__subcategory_name=subcategory)

    if q:
        products = products.filter(
            Q(name__icontains=q) | Q(brand__brand__icontains=q))

    size_list = [size[0] for size in sizes]

    items_per_page = request.GET.get('items_per_page')
    sorting = request.GET.get('order-by')

    if items_per_page:
        items_per_page = int(items_per_page)
    else:
        items_per_page = 12
    if not sorting:
        sorting = 'default'

    match sorting:
        case 'price-asc':
            products = products.order_by('price')
        case 'price-desc':
            products = products.order_by('-price')
        case 'default':
            products = products.order_by('name')

    paginator = Paginator(products, items_per_page)

    page = paginator.get_page(page_number)
    page_count = ceil(len(products) / items_per_page)

    items_per_page_variants = range(6, 25, 6)
    sorting_variants = {
        'price-asc': 'Lowest price before',
        'price-desc': 'Highest price before',
        'default': 'Default'
    }

    context.update({
        'products': page,
        'page_count': range(1, page_count + 1),
        'max_page': page_count,
        'current_page': page_number,
        'items_per_page': items_per_page,
        'items_per_page_variants': items_per_page_variants,
        'sorting': sorting,
        'sorting_variants': sorting_variants,
        'sizes': size_list,
        'subcategories': subcategories,
        'selected_brand': brand,
        'selected_size': size,
        'selected_subcategory': subcategory,
        'selected_category': category,
        'only_in_stock': only_in_stock,
        'q': q,
    })

    return render(request=request, template_name=template_name, context=context)


def product_page(request: HttpRequest, product_id: int):
    template_name = r'eshop/product_page.html'
    product = get_object_or_404(Product, pk=product_id)

    if product.category.category.category_name == 'Footwear':
        sizes = footwear_sizes
    else:
        sizes = wear_sizes

    product_sizes = [size.size for size in product.size_set.all()
                     if size.units_in_stock > 0]

    context.update({
        'product': product,
        'sizes': sizes,
        'product_sizes': product_sizes
    })

    return render(request=request, template_name=template_name, context=context)


@login_required
def add_item_to_cart(request: HttpRequest, product_id: int):
    if request.method == 'POST':
        size = request.POST.get('size')
        product = Size.objects.get(size=size)

        order = Order.objects.filter(user=request.user, status='In cart')
        if order:
            order = order[0]
        else:
            order = Order.objects.create(user=request.user, status='In cart')
            order.save()
            email = request.user.email
            if email:
                subject = 'Your order ' + subjects[order.status]
                send_mail(
                    subject=subject,
                    message=body % (request.user.username, order.id,
                                    subjects[order.status]),
                    recipient_list=[request.user.email],
                    from_email=None
                )

        user_cart = request.user.cart_set.all()
        for item in user_cart:
            if product == item.product:
                break
        else:
            cart = Cart.objects.create(
                user=request.user, product=product)
            order_item = OrderItem.objects.create(
                user=request.user, product=product, order=order)
            cart.save()
            order_item.save()
    messages.add_message(request, messages.SUCCESS,
                         "Item successfully added to cart.")
    return redirect('cart')


@login_required
def shopping_cart(request: HttpRequest):
    template_name = r'eshop/cart.html'
    cart = Cart.objects.filter(user=request.user)
    total = sum(item.product.product.price for item in cart)
    orders = Order.objects.filter(user=request.user)
    order_id = None
    if orders:
        orders = orders.filter(status='In cart')
        if orders:
            order_id = orders[0].id

    context.update({
        'cart': cart,
        'total': total,
        'order_id': order_id
    })

    return render(request=request, template_name=template_name, context=context)


@login_required
def delete_from_cart(request: HttpRequest, item_id: int):
    cart_item = Cart.objects.get(pk=item_id)
    orders = Order.objects.filter(user=request.user)
    if orders:
        orders = orders.filter(status='In cart')
        if orders:
            order = orders[0]
    if order:
        order_items = order.orderitem_set.all()
        for item in order_items:
            if item.product == cart_item.product:
                item.delete()
    cart_item.delete()
    if not order.orderitem_set.all():
        order.delete()

    return redirect('cart')


@login_required
def add_item_to_favourites(request: HttpRequest, product_id: int):
    product = Product.objects.get(pk=product_id)
    user_favourites = request.user.favourite_set.all()
    for item in user_favourites:
        if product == item.product:
            item.delete()
            break
    else:
        favourite = Favourite.objects.create(
            user=request.user, product=product)
        favourite.save()

    messages.add_message(request, messages.SUCCESS,
                         "Item successfully added to favourites.")
    return redirect(request.META.get('HTTP_REFERER'), product_id)


@login_required
def favourites(request: HttpRequest):
    template_name = r'eshop/favourites.html'
    favourites = Favourite.objects.filter(user=request.user)

    context.update({
        'favourites': favourites,
    })

    return render(request=request, template_name=template_name, context=context)


@login_required
def create_review(request: HttpRequest, product_id: int):
    if request.method == 'POST':
        rating = int(request.POST.get('rate'))
        review_text = request.POST.get('review_text')

        product = Product.objects.get(pk=product_id)
        review = Review.objects.create(
            author=request.user, rating=rating, refers_to=product, body=review_text)
        review.save()

        review_images = request.FILES.getlist('review_images')
        for index, image in enumerate(review_images):
            review_image = ReviewImage(
                review=review, image=image, default=True if not index else False)
            review_image.save()

    messages.add_message(request, messages.SUCCESS,
                         "Review successfully created.")
    return redirect(request.META.get('HTTP_REFERER'), product_id)


@login_required
def delete_review(request: HttpRequest, review_id: int):
    review = Review.objects.get(pk=review_id)
    review.delete()

    messages.add_message(request, messages.SUCCESS,
                         "Review successfully deleted.")
    return redirect(request.META.get('HTTP_REFERER'))


@login_required
def order_view(request: HttpRequest, order_id: int):
    template_name = r'eshop/order.html'
    order = Order.objects.get(pk=order_id)

    context.update({
        'order': order,
    })

    return render(request=request, template_name=template_name, context=context)


@login_required
def shipping_info_choice(request: HttpRequest, order_id: int):
    template_name = r'eshop/shipping_info_choice.html'
    shipping_variants = ShippingInfo.objects.filter(user=request.user)
    cities = City.objects.all()
    shipping_companies = ShippingCompany.objects.all()
    departments = Department.objects.all()

    selected_city = request.GET.get('city')
    if selected_city:
        selected_city = int(selected_city)
        departments = departments.filter(department_city_id=selected_city)

    selected_company = request.GET.get('shipping_company')
    if selected_company:
        selected_company = int(selected_company)
        departments = departments.filter(shipping_company_id=selected_company)

    selected_department = request.GET.get('department')
    if selected_department:
        selected_department = int(selected_department)
        selected_department = Department.objects.get(pk=selected_department)
        selected_city = selected_department.department_city.id
        selected_company = selected_department.shipping_company.id
        selected_department = selected_department.id

    context.update({
        'shipping_variants': shipping_variants,
        'cities': cities,
        'shipping_companies': shipping_companies,
        'departments': departments,
        'selected_city': selected_city,
        'selected_company': selected_company,
        'selected_department': selected_department,
        'order_id': order_id
    })

    return render(request=request, template_name=template_name, context=context)


@login_required
def create_shipping_info(request: HttpRequest):
    if request.method == 'POST':
        city = int(request.POST.get('city'))
        department = int(request.POST.get('department'))

        shipping_infos = ShippingInfo.objects.all()

        for info in shipping_infos:
            if department == info.department_id:
                messages.add_message(request, messages.WARNING,
                                     "Shipping info with that data already exists.")
                break
        else:
            shipping_info = ShippingInfo.objects.create(
                city_id=city, department_id=department, user=request.user)
            shipping_info.save()
            messages.add_message(request, messages.SUCCESS,
                                 "Shipping info created successfully.")

        if 'profile' in str(request.META.get("HTTP_REFERER")):
            return redirect('profile')
        return redirect(request.META.get("HTTP_REFERER"))
    else:
        template_name = r'eshop/shipping_info_create.html'

        cities = City.objects.all()
        shipping_companies = ShippingCompany.objects.all()
        departments = Department.objects.all()

        selected_city = request.GET.get('city')
        if selected_city:
            selected_city = int(selected_city)
            departments = departments.filter(department_city_id=selected_city)

        selected_company = request.GET.get('shipping_company')
        if selected_company:
            selected_company = int(selected_company)
            departments = departments.filter(
                shipping_company_id=selected_company)

        selected_department = request.GET.get('department')
        if selected_department:
            selected_department = int(selected_department)
            selected_department = Department.objects.get(
                pk=selected_department)
            selected_city = selected_department.department_city.id
            selected_company = selected_department.shipping_company.id
            selected_department = selected_department.id

        context.update({
            'cities': cities,
            'shipping_companies': shipping_companies,
            'departments': departments,
            'selected_city': selected_city,
            'selected_company': selected_company,
            'selected_department': selected_department,
        })

        return render(request=request, template_name=template_name, context=context)


@login_required
def update_shipping_info(request: HttpRequest, info_id: int):
    info = ShippingInfo.objects.get(pk=info_id)
    if request.method == 'POST':
        city = int(request.POST.get('city'))
        department = int(request.POST.get('department'))

        info.city_id = city
        info.department_id = department
        info.save()
        messages.add_message(request, messages.SUCCESS,
                             "Shipping info updated successfully.")
        return redirect('profile')
    else:
        template_name = r'eshop/shipping_info_update.html'

        cities = City.objects.all()
        shipping_companies = ShippingCompany.objects.all()
        departments = Department.objects.all()

        selected_city = request.GET.get('city')
        if selected_city:
            selected_city = int(selected_city)
            departments = departments.filter(department_city_id=selected_city)
        else:
            selected_city = info.city_id

        selected_company = request.GET.get('shipping_company')
        if selected_company:
            selected_company = int(selected_company)
            departments = departments.filter(
                shipping_company_id=selected_company)
        else:
            selected_company = info.department.shipping_company_id

        selected_department = request.GET.get('department')
        if selected_department:
            selected_department = int(selected_department)
            selected_department = Department.objects.get(
                pk=selected_department)
            selected_city = selected_department.department_city.id
            selected_company = selected_department.shipping_company.id
            selected_department = selected_department.id
        else:
            selected_department = info.department_id

        context.update({
            'info': info,
            'cities': cities,
            'shipping_companies': shipping_companies,
            'departments': departments,
            'selected_city': selected_city,
            'selected_company': selected_company,
            'selected_department': selected_department,
        })
        return render(request=request, template_name=template_name, context=context)


@login_required
def delete_shipping_info(request: HttpRequest, info_id: int):
    info = ShippingInfo.objects.get(pk=info_id)

    if info.order_set.all():
        messages.add_message(request, messages.ERROR,
                             "There are orders with this shipping info.")
    else:
        messages.add_message(request, messages.SUCCESS,
                             "Shipping info deleted successfully.")
        info.delete()

    return redirect(request.META.get("HTTP_REFERER"))


@login_required
def add_shipping_info_to_order(request: HttpRequest, order_id: int):
    if request.method == 'POST':
        shipping_info = request.POST.get('shipping_variant')
        shipping_info = ShippingInfo.objects.get(pk=shipping_info)
        order = Order.objects.get(pk=order_id)
        order.status = 'Confirmed'
        order.ship_to = shipping_info
        order.save()
        email = request.user.email
        if email:
            subject = 'Your order ' + subjects[order.status]
            send_mail(
                subject=subject,
                message=body % (request.user.username, order.id,
                                subjects[order.status]),
                recipient_list=[request.user.email],
                from_email=None
            )

        messages.add_message(request, messages.SUCCESS,
                             "Shipping info successfully added to your order.")
        return redirect('payment', order_id)


@login_required
def payment(request: HttpRequest, order_id: int):
    order = Order.objects.get(pk=order_id)
    order.status = 'Paid'
    for item in order.orderitem_set.all():
        product = item.product
        product.units_in_stock -= 1
        product.save()
    for item in request.user.cart_set.all():
        item.delete()
    order.save()
    email = request.user.email
    if email:
        subject = 'Your order ' + subjects[order.status]
        send_mail(
            subject=subject,
            message=body % (request.user.username, order.id,
                            subjects[order.status]),
            recipient_list=[request.user.email],
            from_email=None
        )
    messages.add_message(request, messages.SUCCESS,
                         "I'm joking, it's portfolio site, there's no payment system :)")
    return redirect('order_view', order_id)


@login_required
def send_order(request: HttpRequest, order_id: int):
    order = Order.objects.get(pk=order_id)
    order.status = 'Sent'
    order.save()
    email = request.user.email
    if email:
        subject = 'Your order ' + subjects[order.status]
        send_mail(
            subject=subject,
            message=body % (request.user.username, order.id,
                            subjects[order.status]),
            recipient_list=[request.user.email],
            from_email=None
        )
    messages.add_message(request, messages.SUCCESS,
                         "It's still just portfolio site :)")
    return redirect('order_view', order_id)


@login_required
def complete_order(request: HttpRequest, order_id: int):
    order = Order.objects.get(pk=order_id)
    order.status = 'Completed'
    order.save()
    email = request.user.email
    if email:
        subject = 'Your order ' + subjects[order.status]
        send_mail(
            subject=subject,
            message=body % (request.user.username, order.id,
                            subjects[order.status]),
            recipient_list=[request.user.email],
            from_email=None
        )
    messages.add_message(request, messages.SUCCESS,
                         "It's still just portfolio site :)")
    return redirect('order_view', order_id)


@login_required
def delete_order(request: HttpRequest, order_id: int):
    order = Order.objects.get(pk=order_id)
    if order.status in ('In cart', 'Confirmed'):
        order.delete()
        messages.add_message(request, messages.SUCCESS,
                             "Order deleted successfully.")

    return redirect('profile')
