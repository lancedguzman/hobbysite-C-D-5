from django.db import models
from user_management.models import Profile


class ProductType(models.Model):
    """Creates the ProductType Model."""
    name = models.CharField(max_length=255, default="")
    description = models.TextField()

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Product(models.Model):
    """Creates the Product Model."""
    STATUS_CHOICES = (
        ("AVAILABLE", "Available"),
        ("ONSALE", "On Sale"),
        ("OUTOFSTOCK", "Out of Stock"),
    )

    name = models.CharField(max_length=255)
    product_type = models.ForeignKey(ProductType, on_delete=models.SET_NULL,
                                     null=True, related_name="producttype")
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE)
    description = models.TextField()
    price = models.DecimalField(max_digits=7, decimal_places=2)
    stock = models.IntegerField()
    status = models.CharField(choices=STATUS_CHOICES, default="AVAILABLE")
    image = models.CharField(max_length=255)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name
    

class Transaction(models.Model):
    """Creates the Transaction Model."""
    STATUS_CHOICES = (
        ("ONCART", "On Cart"),
        ("TOPAY", "To Pay"),
        ("TOSHIP", "To Ship"),
        ("TORECEIVE", "To Receive"),
        ("DELIVERED", "Delivered"),
    )

    buyer = models.ForeignKey(Profile, on_delete=models.SET_NULL,
                              null=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL,
                                related_name="product", null=True)
    amount = models.IntegerField()
    status = models.CharField(choices=STATUS_CHOICES)
    CreatedOn = models.DateTimeField(auto_now=True)


def process_transaction(product, amount):
    """Function to reduce amount of stock per transaction."""
    if (product.stock >= amount):
        product.stock -= amount
        product.status = "OUTOFSTOCK" if product.stock == 0 else "AVAILABLE"
        product.save()
    
    else:
        raise ValueError("Not enough stock.")
