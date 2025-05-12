from django.urls import path
from . views import *

app_name = 'merchstore'

urlpatterns = [
    path('', home_page, name='home_page'),
    path('merchstore/items/', product_list, name='product_list'),
    path('merchstore/item/<int:product_id>', product_detail, name='product_detail'),
    path('merchstore/item/add', product_create, name='product_create'),
    path('merchstore/item/<int:product_id>/edit', product_update, name='product_update'),
    path('merchstore/cart', cart, name='cart'),
    path('merchstore/transactions', transaction_list, name='transactions'),
]
