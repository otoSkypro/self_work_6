from django.contrib import messages
from django.views import View
from django.shortcuts import render, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Product, Contact
from .forms import ProductForm


class ProductListView(View):
    def get(self, request):
        products = Product.objects.all()
        paginator = Paginator(products, 10)  # По 10 продуктов на страницу
        page = request.GET.get('page')
        try:
            products = paginator.page(page)
        except PageNotAnInteger:
            products = paginator.page(1)
        except EmptyPage:
            products = paginator.page(paginator.num_pages)
        return render(request, 'product_list.html', {'products': products})


class CreateProductView(View):
    def get(self, request):
        form = ProductForm()
        return render(request, 'create_product.html', {'form': form})

    def post(self, request):
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('catalog:home')
        return render(request, 'create_product.html', {'form': form})


class HomeView(View):
    def get(self, request):
        latest_products = Product.objects.order_by('-created_at')[:5]
        for product in latest_products:
            print(f'ID: {product.id}, Name: {product.name}, Price: {product.price}')
        return render(request, 'home.html', {'latest_products': latest_products})


class ContactsView(View):
    def get(self, request):
        contacts = Contact.objects.all()
        context = {'contacts': contacts}
        return render(request, 'contacts.html', context)


class SubmitFeedbackView(View):
    def post(self, request):
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        message = request.POST.get('message')
        contact = Contact.objects.create(name=name, phone=phone, message=message)
        messages.success(request, 'Ваше сообщение успешно отправлено!')
        print(f'Имя: {name}\nТелефон: {phone}\nСообщение: {message}')
        return redirect('catalog:contacts')


class ProductDetailView(View):
    def get(self, request, product_id):
        product = Product.objects.get(pk=product_id)
        return render(request, 'product_detail.html', {'product': product})