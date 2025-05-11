from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Product, Transaction, process_transaction
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.urls import reverse
from .forms import ProductForm, UpdateForm, TransactionForm

def home_page(request):
    """Displays the homepage with links to each app."""
    return render(request, "home_page.html")


def product_list(request):
    """Displays the product list page."""
    user_products = Product.objects.none()
    other_products = Product.objects.all()

    if (request.user.is_authenticated):
        user_profile = request.user.profile
        user_products = Product.objects.filter(owner=user_profile)
        other_products =Product.objects.exclude(owner=user_profile)

    return render(request, "product_list.html", {
        "user_products": user_products,
        "other_products": other_products,
        })


def product_detail(request, product_id):
    """Displays the product details and Transaction Form."""
    product = get_object_or_404(Product, id=product_id)

    if (request.method == "POST"):
        if (not request.user.is_authenticated):
            login_url = reverse("user_management:login")
            return redirect(f"{login_url}?{REDIRECT_FIELD_NAME}={request.path}")
        
        form = TransactionForm(request.POST)

        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.product = product
            transaction.buyer = request.user.profile
            process_transaction(product, transaction.amount)
            transaction.save()
            return redirect("merchstore:cart")
        
    else:
        form = TransactionForm()

    return render(request, "product_detail.html", {
        "product": product,
        "transaction_form": form,
        })


@login_required
def product_create(request):
    """Displays the Product Create Form."""
    if (request.method == "POST"):
        form = ProductForm(request.POST)

        if form.is_valid():
            product = form.save(commit=False)
            product.owner = request.user.profile
            product.save()
            return redirect("merchstore:product_list")
    else:
        form = ProductForm()

    return render(request, "product_form.html",
                  {"product_form": form})


@login_required
def product_update(request, product_id):
    """Displays the Product Update Form."""
    product = get_object_or_404(Product, id=product_id)

    if (request.method == "POST"):
        form = UpdateForm(request.POST, instance=product)

        if form.is_valid():
            form.save()
            return redirect("merchstore:product_list")
        
    else:
        form = UpdateForm(instance=product)

    return render(request, "update_form.html", {
        "update_form": form,
        "product": product
    })


@login_required
def cart(request):
    """Displays the Transaction list of user as the buyer."""
    user_transactions = Transaction.objects.none()

    if (request.user.is_authenticated):
        user_profile = request.user.profile
        user_transactions = Transaction.objects.filter(buyer=user_profile)

    return render(request, "cart.html", {
        "user_transactions": user_transactions})


@login_required
def transaction_list(request):
    """Displays the Transaction list of user as the seller."""
    user_transactions = Transaction.objects.none()

    if (request.user.is_authenticated):
        user_profile = request.user.profile
        user_transactions = Transaction.objects.exclude(buyer=user_profile)
        
    return render(request, "transaction_list.html",
                  {"user_transactions": user_transactions})
