from django.contrib import admin
from .models import ProductType, Product, Transaction

class ProductTypeAdmin(admin.ModelAdmin):
    """Creates the ProductType Admin Panel."""
    model = ProductType

    list_display = ('name', 'description',)
    search_fields = ('name',)
    ordering = ('name',)


class ProductAdmin(admin.ModelAdmin):
    """Creates the Product Admin Panel."""
    model = Product

    list_display = ('name', 'product_type',
                    'owner', 'description',
                    'price','stock',
                    'status')
    list_filter = ('product_type',)
    search_fields = ('name', 'product_type',)
    ordering = ('name',)
    list_editable = ('price','stock',)


class TransactionAdmin(admin.ModelAdmin):
    """Creates the Transaction Admin Panel."""
    model = Transaction

    list_display = ('buyer', 'product',
                    'amount', 'status',
                    'CreatedOn',)


admin.site.register(ProductType, ProductTypeAdmin)

admin.site.register(Product, ProductAdmin)

admin.site.register(Transaction, TransactionAdmin)
