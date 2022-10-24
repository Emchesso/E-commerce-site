from django.contrib.auth.models import User
from django.db import models

class Admin(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=50)
    image = models.ImageField(upload_to="admins")
    phone = models.CharField(max_length=20)

    def __str__(self):
        return self.user.username

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=200)
    address = models.CharField(max_length=200, null=True, blank=True)
    joined_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.full_name

class Category(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.title
    
class Product(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE) # 1-m Product to Category
    image = models.ImageField(upload_to="products")
    marked_price = models.FloatField()
    selling_price = models.FloatField()
    description = models.TextField()
    # warranty = models.CharField(max_length=300, null=True, blank=True)
    # return_policy = models.CharField(max_length=300, null=True, blank=True)
    view_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title

class Cart(models.Model):
    customer = models.ForeignKey(
        Customer, on_delete=models.SET_NULL, null=True, blank=True) #1-1 Customer to Cart
    total = models.FloatField(default = 0)
    created_at =  models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "Cart: " + str(self.id)

class CartProduct(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE) # 1-m Cart to Product
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    rate = models.FloatField()
    quantity = models.PositiveIntegerField()
    subtotal = models.FloatField()

    def __str__(self):
        return "Cart: " + str(self.cart.id) + "CartProduct: " + str(self.id)

ORDER_STATUS = ( # first value in db, second in form
    ("Order Placed", "Order Placed"),
    ("Order Processing", "Order Processing"),
    ("Delivery in Progress", "Delivery in Progress"),
    ("Order Complete", "Order Complete"),
    ("Order Cancelled", "Order Cancelled"),
)

class Order(models.Model):
    cart = models.OneToOneField(Cart, on_delete=models.CASCADE)
    ordered_by = models.CharField(max_length=200)
    shipping_address = models.CharField(max_length=200)
    phone = models.CharField(max_length=10)
    email = models.EmailField(null=True, blank=True)
    subtotal = models.FloatField()
    discount = models.FloatField()
    total = models.FloatField()
    order_status = models.CharField(max_length=50, choices=ORDER_STATUS)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "Order: " + str(self.id)