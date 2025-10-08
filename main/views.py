from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.core import serializers
from main.models import Product
from main.forms import ProductForm
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import datetime
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.utils.html import strip_tags

@login_required(login_url='/login')
def show_main(request):
    context = {
        'nama_toko' : 'Jual Bola DLL',
        'last_login': request.COOKIES.get('last_login', 'Never'),
    }
    return render(request, "main.html", context)

@login_required(login_url='/login')
def create_product(request):
    form = ProductForm(request.POST or None)
    if form.is_valid() and request.method == "POST":
        product_entry = form.save(commit=False)
        product_entry.user = request.user
        product_entry.save()
        return redirect('main:show_main')
    context = {'form': form}
    return render(request, "create_product.html", context)

@login_required(login_url='/login')
def edit_product(request, id):
    product = get_object_or_404(Product, pk=id)
    if product.user != request.user:
        messages.error(request, "You are not authorized to edit this product.")
        return redirect('main:show_main')
    form = ProductForm(request.POST or None, instance=product)
    if form.is_valid() and request.method == 'POST':
        form.save()
        return redirect('main:show_main')
    context = {'form': form}
    return render(request, "edit_product.html", context)

@login_required(login_url='/login')
def delete_product(request, id):
    product = get_object_or_404(Product, pk=id)
    if product.user != request.user:
        messages.error(request, "You are not authorized to delete this product.")
        return redirect('main:show_main')
    product.delete()
    return HttpResponseRedirect(reverse('main:show_main'))

@login_required(login_url='/login')
def show_product(request, id):
    context = {'product_id': id}
    return render(request, "product_detail.html", context)

def show_xml(request):
    product_list = Product.objects.all()
    return HttpResponse(serializers.serialize("xml", product_list), content_type="application/xml")

def show_json(request):
    product_list = Product.objects.select_related('user').all()
    data = [{
        'pk': str(product.pk),
        'fields': {
            'name': product.name, 'price': product.price, 'description': product.description,
            'thumbnail': product.thumbnail, 'category': product.category, 'is_featured': product.is_featured,
            'user_id': product.user.id if product.user else None,
        }
    } for product in product_list]
    return JsonResponse(data, safe=False)

def show_xml_by_id(request, product_id):
    product_item = Product.objects.filter(pk=product_id)
    return HttpResponse(serializers.serialize("xml", product_item), content_type="application/xml")

def show_json_by_id(request, product_id):
    try:
        product = Product.objects.select_related('user').get(pk=product_id)
        data = {
            'pk': str(product.pk),
            'fields': {
                'name': product.name, 'price': product.price, 'description': product.description,
                'thumbnail': product.thumbnail, 'category': product.category, 'is_featured': product.is_featured,
                'user_id': product.user.id if product.user else None,
                'username': product.user.username if product.user else "Anonymous",
            }
        }
        return JsonResponse(data)
    except Product.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Product not found'}, status=404)

def register(request):
    form = UserCreationForm()
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your account has been successfully created!')
            return redirect('main:login')
    context = {'form': form}
    return render(request, 'register.html', context)

def login_user(request):
   if request.method == 'POST':
      form = AuthenticationForm(data=request.POST)
      if form.is_valid():
        user = form.get_user()
        login(request, user)
        response = HttpResponseRedirect(reverse("main:show_main"))
        response.set_cookie('last_login', str(datetime.datetime.now()))
        return response
   else:
      form = AuthenticationForm(request)
   context = {'form': form}
   return render(request, 'login.html', context)

def logout_user(request):
    logout(request)
    response = HttpResponseRedirect(reverse('main:login'))
    response.delete_cookie('last_login')
    return response

@csrf_exempt
@require_POST
@login_required
def add_product_ajax(request):
    name = strip_tags(request.POST.get("name"))
    price = request.POST.get("price")
    description = strip_tags(request.POST.get("description"))
    Product.objects.create(
        user=request.user, name=name, price=price, description=description,
        thumbnail=request.POST.get("thumbnail"), category=request.POST.get("category"),
        is_featured=request.POST.get("is_featured") == 'on'
    )
    return HttpResponse(b"CREATED", status=201)

@csrf_exempt
@require_POST
@login_required
def delete_product_ajax(request, id):
    try:
        product = Product.objects.get(pk=id)
        if product.user != request.user:
            return JsonResponse({"status": "error", "message": "Not authorized."}, status=403)
        product.delete()
        return JsonResponse({"status": "success", "message": "Product deleted."}, status=200)
    except Product.DoesNotExist:
        return JsonResponse({"status": "error", "message": "Product not found."}, status=404)
    
@csrf_exempt
@login_required
def edit_product_ajax(request, id):
    product = get_object_or_404(Product, pk=id)

    if product.user != request.user:
        return JsonResponse({'status': 'error', 'message': 'Not authorized.'}, status=403)

    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return JsonResponse({'status': 'success', 'message': 'Product updated successfully!'})
        else:
            return JsonResponse({'status': 'error', 'errors': form.errors}, status=400)
    
    data = {
        'name': product.name, 'price': product.price, 'description': product.description,
        'thumbnail': product.thumbnail, 'category': product.category, 'is_featured': product.is_featured
    }
    return JsonResponse(data)

@csrf_exempt
def register_ajax(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({'status': 'success', 'message': 'Account created successfully!'}, status=201)
        else:
            return JsonResponse({'status': 'error', 'errors': form.errors}, status=400)
    return JsonResponse({'status': 'fail'}, status=405)

@csrf_exempt
def login_ajax(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return JsonResponse({'status': 'success', 'message': 'Login successful!', 'username': user.username})
        else:
            return JsonResponse({'status': 'error', 'message': 'Invalid username or password.'}, status=400)
    return JsonResponse({'status': 'fail'}, status=405)