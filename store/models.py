from django.db import models
import datetime

# Create your models here.
def get_file_path(request, filename):
    original_filename = filename
    nowtime = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    filename = f"{nowtime}_{original_filename}"
    return f"uploads/{filename}"

class Category(models.Model):
    slug = models.CharField(max_length=50, null=False, blank=False)
    name = models.CharField(max_length=50, null=False, blank=False)
    image = models.ImageField(upload_to=get_file_path, null=False, blank=False)
    description = models.TextField(max_length=500, null=False, blank=False)
    status = models.BooleanField(default=False, null=True, blank=False)
    trending = models.BooleanField(default=False, null=True, blank=False)
    meta_title = models.CharField(max_length=150, null=False, blank=False)
    meta_keywords = models.CharField(max_length=150, null=False, blank=False)
    meta_description = models.CharField(max_length=150, null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name

class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    slug = models.CharField(max_length=50, null=False, blank=False)
    name = models.CharField(max_length=50, null=False, blank=False)
    product_image = models.ImageField(upload_to=get_file_path, null=False, blank=False)
    small_description = models.CharField(max_length=150, null=False, blank=False)
    quantity = models.IntegerField(null=False, blank=False)
    description = models.TextField(max_length=500, null=False, blank=False)
    original_price = models.FloatField(null=False, blank=False)
    selling_price = models.FloatField(null=False, blank=False)
    status = models.BooleanField(default=False, null=True, blank=False)
    trending = models.BooleanField(default=False, null=True, blank=False)
    tag = models.CharField(max_length=150, null=False, blank=False)
    meta_title = models.CharField(max_length=150, null=False, blank=False)
    meta_keywords = models.CharField(max_length=150, null=False, blank=False)
    meta_description = models.CharField(max_length=150, null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    


class Cart(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    product_qty = models.IntegerField(null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.product.name} - {self.product_qty}"
    

class order(models.Model):
    first_name = models.CharField(max_length=50, null=False, blank=False)
    last_name = models.CharField(max_length=50, null=False, blank=False)
    email = models.CharField(max_length=50, null=False, blank=False)
    phone = models.CharField(max_length=50, null=False, blank=False)
    address = models.TextField(max_length=500, null=False, blank=False)
    city = models.CharField(max_length=50, null=False, blank=False)
    state = models.CharField(max_length=50, null=False, blank=False)
    country = models.CharField(max_length=50, null=False, blank=False)
    pincode = models.CharField(max_length=50, null=False, blank=False)
    total_price = models.FloatField(null=False, blank=False)
    payment_mode = models.CharField(max_length=50, null=False, blank=False)
    payment_id = models.CharField(max_length=150, null=True, blank=True)
    order_status = models.CharField(max_length=50, null=False, blank=False, default='Pending')
    message = models.TextField(max_length=500, null=True, blank=True)
    tracking_no = models.CharField(max_length=150, null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)


    def __str__(self):
        return f"{self.user.username} - {self.tracking_no}"
    

class OrderItem(models.Model):
    order = models.ForeignKey(order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.FloatField(null=False, blank=False)
    quantity = models.IntegerField(null=False, blank=False)

    def __str__(self):
        return f"{self.order.tracking_no} - {self.product.name}"
    
