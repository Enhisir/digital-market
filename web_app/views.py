from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse, HttpResponseNotFound, HttpResponseNotAllowed
from django.shortcuts import render, redirect, get_object_or_404

from web_app.forms import RegistrationForm, LoginForm, ProductForm, \
    EditProductForm
from web_app.models import User, Product


def main_view(request):
    return render(request,
                  "web_app/main.html",
                  {"products": Product.objects.all(), })


def registration_view_post(request: HttpRequest) -> HttpResponse:
    form = RegistrationForm(data=request.POST)

    if form.is_valid():
        user = User(
            username=form.cleaned_data['username'],
            email=form.cleaned_data['email'])
        user.set_password(form.cleaned_data["password"])
        user.save()
        print(form.cleaned_data)
        return redirect("/login")
    else:
        return render(
            request,
            "web_app/registration.html",
            {"form": form})


def registration_view(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        return registration_view_post(request)

    form = RegistrationForm()
    return render(
        request,
        "web_app/registration.html",
        {"form": form})


def login_view_post(request: HttpRequest) -> HttpResponse:
    form = LoginForm(data=request.POST)

    if form.is_valid():
        user = authenticate(**form.cleaned_data)
        if user is not None:
            login(request, user)
            print(form.cleaned_data)
            return redirect("/")
        else:
            form.add_error(None, "Неверные имя или пароль")

    return render(
        request,
        "web_app/login.html",
        {"form": form})


def login_view(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        return login_view_post(request)

    form = LoginForm()
    return render(
        request,
        "web_app/login.html",
        {"form": form})


def logout_view(request: HttpRequest) -> HttpResponse:
    logout(request)
    return redirect("/")


@staff_member_required()
def add_product_view_post(request: HttpRequest) -> HttpResponse:
    form = ProductForm(data=request.POST, files=request.FILES)

    if form.is_valid():
        print(form.cleaned_data)
        product = Product(**form.cleaned_data)
        product.save()
        return redirect("/")

    return render(
        request,
        "web_app/add_product.html",
        {"form": form})


@staff_member_required()
def add_product_view(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        return add_product_view_post(request)

    form = ProductForm()
    return render(
        request,
        "web_app/add_product.html",
        {"form": form})


@staff_member_required()
def manage_product_view_update(
        request: HttpRequest,
        _id: int = None) -> HttpResponse:
    product = get_object_or_404(Product, id=_id)

    form = EditProductForm(data=request.POST, instance=product, files=request.FILES)
    if form.is_valid():
        # product._do_update(**form.cleaned_data)
        # product.save()
        form.save()
        return redirect("/")

    return render(
        request,
        "web_app/add_product.html",
        {"form": form})


# @staff_member_required()
# def manage_product_view_delete(
#         request: HttpRequest,
#         _id: int = None) -> HttpResponse:
#     product = get_object_or_404(Product, id=_id)
#     product.delete()
#     return redirect("/")


@staff_member_required()
def manage_product_view(
        request: HttpRequest,
        _id: int = None) -> HttpResponse:
    if request.method == "POST":
        return manage_product_view_update(request, _id=_id)

    # if request.method == "DELETE":
    #     return manage_product_view_delete(request, _id=_id)

    product = get_object_or_404(Product, id=_id)
    form = EditProductForm(instance=product)
    return render(
        request,
        "web_app/add_product.html",
        {"form": form})
