from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

wear_sizes = [
    ('S', 'S'),
    ('M', 'M'),
    ('L', 'L'),
    ('XL', 'XL')
]

footwear_sizes = []

for i in range(6, 12):
    footwear_sizes.append((str(i)+'US', str(i)+'US'))
    footwear_sizes.append((str(i+0.5)+'US', str(i+0.5)+'US'))

sizes = wear_sizes + footwear_sizes

statuses = [
    ('In cart', 'In cart'),
    ('Confirmed', 'Confirmed'),
    ('Paid', 'Paid'),
    ('Sent', 'Sent'),
    ('Completed', 'Completed'),
]


class Brand(models.Model):
    brand = models.CharField(max_length=50, verbose_name='Brand Name', unique=True)

    def __str__(self):
        return self.brand


class Category(models.Model):
    category_name = models.CharField(
        max_length=25, verbose_name='Category Name', unique=True)

    def __str__(self):
        return self.category_name


class SubCategory(models.Model):
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, verbose_name='Category')
    subcategory_name = models.CharField(
        max_length=25, verbose_name='Subcategory Name')

    class Meta:
        unique_together = ('category', 'subcategory_name')

    def __str__(self):
        return f'{self.category.category_name} - {self.subcategory_name}'


class Product(models.Model):
    name = models.CharField(max_length=50, verbose_name='Name')
    brand = models.ForeignKey(
        Brand, on_delete=models.CASCADE, verbose_name='Brand')
    price = models.DecimalField(max_digits=7, decimal_places=2, validators=[
                                MinValueValidator(0)], verbose_name='Price ($)')
    category = models.ForeignKey(
        SubCategory, on_delete=models.CASCADE, blank=True, null=True, verbose_name='Category')
    description = models.TextField(verbose_name='Description')

    def __str__(self):
        return f'{self.brand} {self.name}'

    def info(self):
        return f'{ self.brand } {self.name}'

    def image(self):
        main_image = self.itemimage_set.filter(default=True)
        if main_image:
            return main_image[0].image
        else:
            return False

    def in_stock(self):
        return sum(item.units_in_stock for item in self.size_set.all())

    def rating(self):
        set = self.review_set.all()
        if set:
            avg = round(sum(item.rating for item in set) / len(set))
        else:
            return '☆' * 5
        return (avg * '★') + ((5 - avg) * '☆')
    
    def in_favourites(self):
        if self.favourite_set.all():
            return True
        return False


class Size(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, verbose_name='Choose Product')
    units_in_stock = models.PositiveIntegerField(
        verbose_name='Number in Stock')
    size = models.CharField(choices=sizes, max_length=10, verbose_name='Size')

    class Meta:
        unique_together = ('product', 'size')

    def __str__(self):
        return f'{self.product.name}. {self.size} Size.'


class ItemImage(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, verbose_name='Product')
    image = models.ImageField(
        upload_to='items/uploads', verbose_name='Upload an Image')
    default = models.BooleanField(
        default=False, verbose_name='Use as main image')

    def __str__(self):
        return f'Image for {self.product}'


class Review(models.Model):
    refers_to = models.ForeignKey(
        Product, on_delete=models.CASCADE, verbose_name='Review on')
    author = models.ForeignKey(
        'auth.User', on_delete=models.CASCADE, verbose_name='Nickname')
    rating = models.PositiveIntegerField(
        verbose_name='Your Rating', validators=[MaxValueValidator(5)])
    body = models.TextField(verbose_name='Comments')
    
    def stars(self):
        return (self.rating * '★') + ((5 - self.rating) * '☆')
    
    def __str__(self):
        return f'{self.refers_to.name}. {self.author} - {self.stars()} Star review.'


class ReviewImage(models.Model):
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, verbose_name='Product')
    image = models.ImageField(
        upload_to='reviews/uploads', verbose_name='Upload an Image', null=True)
    default = models.BooleanField(
        default=False, verbose_name='Use as main image')

    def __str__(self):
        return f'Image for {self.review}'


class Country(models.Model):
    country = models.CharField(max_length=25)

    def __str__(self):
        return self.country


class City(models.Model):
    country = models.ForeignKey(
        Country, on_delete=models.CASCADE, verbose_name='Country')
    city = models.CharField(max_length=25)

    def __str__(self):
        return f'{self.city}, {self.country}'


class ShippingCompany(models.Model):
    company_name = models.CharField(
        max_length=50, verbose_name='Shipping Company Name')

    def __str__(self):
        return self.company_name


class Department(models.Model):
    shipping_company = models.ForeignKey(
        ShippingCompany, on_delete=models.CASCADE, verbose_name='Shipping Company')
    department_city = models.ForeignKey(
        City, on_delete=models.CASCADE)
    department_number = models.PositiveIntegerField(
        verbose_name='Department Name')
    department_address = models.TextField(verbose_name='Department Address')

    def __str__(self):
        return f'{self.shipping_company} department #{self.department_number}. {self.department_address}, {self.department_city}'


class ShippingInfo(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, verbose_name='User')
    city = models.ForeignKey(
        City, on_delete=models.CASCADE, verbose_name='City')
    department = models.ForeignKey(
        Department, on_delete=models.CASCADE, verbose_name='Shipping Department')

    def __str__(self):
        return f'{self.user}. Ship to {self.department}'


class Favourite(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, verbose_name='User')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Product')

    class Meta:
        unique_together = ('user', 'product')

    def __str__(self):
        return f'{self.user}. {self.product}'
    
class Order(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, verbose_name='User')
    status = models.CharField(choices=statuses, max_length=15, verbose_name='Status')
    ship_to = models.ForeignKey(ShippingInfo, on_delete=models.SET_NULL, null=True, verbose_name='Ship to')

    def total(self):
        return sum(item.product.product.price for item in self.orderitem_set.all())

    def __str__(self):
        return f'{self.user} {self.status} order. Ship to {self.ship_to if self.ship_to else "#"}'

class OrderItem(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, verbose_name='User')
    product = models.ForeignKey(Size, on_delete=models.CASCADE, verbose_name='Product')
    order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name='Order')

    def __str__(self):
        return f'{self.user}. {self.product.product} {self.product.size}'

class Cart(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, verbose_name='User')
    product = models.ForeignKey(Size, on_delete=models.CASCADE, verbose_name='Product')

    class Meta:
        unique_together = ('user', 'product')

    def __str__(self):
        return f'{self.user}. {self.product.product} {self.product.size}'
