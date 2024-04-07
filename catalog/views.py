# catalog/views.py
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, Contact, Version
from .forms import ProductForm, VersionForm
from django.contrib import messages
from django.views import View
from django.core.cache import cache


class ProductListView(View):
    def get(self, request):
        # Упорядочиваем продукты по id перед пагинацией
        products = Product.objects.all().order_by('id')

        # Добавляем информацию об активной версии для каждого продукта
        for product in products:
            active_version = Version.objects.filter(product=product, is_active=True).first()
            product.active_version = active_version

        # Форма для добавления новой версии
        version_form = VersionForm()

        paginator = Paginator(products, 4)  # По 4 продукта на страницу
        page = request.GET.get('page')
        try:
            products = paginator.page(page)
        except PageNotAnInteger:
            products = paginator.page(1)
        except EmptyPage:
            products = paginator.page(paginator.num_pages)

        return render(request, 'product_list.html', {'products': products, 'version_form': version_form})


class CreateProductView(View):
    def get(self, request):
        form = ProductForm()
        version_form = VersionForm()
        return render(request, 'create_product.html', {'form': form, 'version_form': version_form})

    def post(self, request):
        form = ProductForm(request.POST, request.FILES)
        version_form = VersionForm(request.POST)

        if form.is_valid() and version_form.is_valid():
            product = form.save()
            product.user = self.request.user
            product.save()
            version = version_form.save(commit=False)
            version.product = product
            version.save()
            return redirect('catalog:product_detail', product_id=product.id)

        return render(request, 'create_product.html', {'form': form, 'version_form': version_form})


class EditProductView(View):
    def get(self, request, product_id):
        product = get_object_or_404(Product, pk=product_id)

        # Проверяем, является ли текущий пользователь владельцем продукта
        if not product.is_owner(request.user):
            messages.error(request, 'У вас нет прав для редактирования этого продукта.')
            return redirect('catalog:product_list')

        form = ProductForm(instance=product)
        return render(request, 'edit_product.html', {'form': form, 'product': product})

    def post(self, request, product_id):
        product = get_object_or_404(Product, pk=product_id)

        # Проверяем, является ли текущий пользователь владельцем продукта
        if not product.is_owner(request.user):
            messages.error(request, 'У вас нет прав для редактирования этого продукта.')
            return redirect('catalog:product_list')

        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.error(request, 'Продукт успешно отредактирован.')  # Здесь изменено
            return redirect('catalog:product_detail', product_id=product_id)
        return render(request, 'edit_product.html', {'form': form, 'product': product})


class DeleteProductView(View):
    def get(self, request, product_id):
        product = get_object_or_404(Product, pk=product_id)
        return render(request, 'delete_product.html', {'product': product})

    def post(self, request, product_id):
        product = get_object_or_404(Product, pk=product_id)
        product.delete()
        messages.success(request, 'Продукт успешно удален.')
        return redirect('catalog:product_list')


class HomeView(View):
    def get(self, request):
        latest_products = Product.objects.order_by('-created_at')[:5]
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
        return redirect('catalog:contacts')


class ProductDetailView(View):
    def get(self, request, product_id):
        product = cache.get(f'product_{product_id}')

        if not product:
            # Если продукт не найден в кеше, получаем его из базы данных и кешируем
            product = Product.objects.get(pk=product_id)
            cache.set(f'product_{product_id}', product)

        versions = Version.objects.filter(product=product)
        version_form = VersionForm()

        return render(request, 'product_detail.html', {'product': product, 'versions': versions, 'version_form': version_form})

    def post(self, request, product_id):
        product = Product.objects.get(pk=product_id)
        versions = Version.objects.filter(product=product)
        version_form = VersionForm(request.POST)

        if version_form.is_valid():
            version = version_form.save(commit=False)
            version.product = product
            version.save()
            return redirect('catalog:product_detail', product_id=product_id)

        return render(request, 'product_detail.html', {'product': product, 'versions': versions, 'version_form': version_form})


class AddVersionView(View):
    def post(self, request):
        version_form = VersionForm(request.POST)

        if version_form.is_valid():
            product_id = request.POST.get('product_id')  # Добавьте поле product_id в форму
            product = Product.objects.get(pk=product_id)

            # Деактивируем текущую активную версию продукта
            Version.objects.filter(product=product, is_active=True).update(is_active=False)

            # Создаем новую версию и делаем ее активной
            version = version_form.save(commit=False)
            version.product = product
            version.is_active = True
            version.save()

        return redirect('catalog:product_list')
