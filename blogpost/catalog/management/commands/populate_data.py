import os
from django import setup

# Установка переменной окружения для Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Django_Web_Store.settings")

# Инициализация Django
setup()

from django.core.management.base import BaseCommand
from django.db import transaction
from catalog.models import Category, Product
from faker import Faker
import random

fake = Faker()


class Command(BaseCommand):
    help = 'Populate database with sample data'

    def handle(self, *args, **options):
        with transaction.atomic():
            self.stdout.write(self.style.SUCCESS('Clearing existing data...'))
            Category.objects.all().delete()
            Product.objects.all().delete()

            self.stdout.write(self.style.SUCCESS('Populating data...'))

            # Creating categories
            electronics = Category.objects.create(name='Electronics', description='Electronic devices')
            clothing = Category.objects.create(name='Clothing', description='Fashion and apparel')
            books = Category.objects.create(name='Books', description='Books and literature')

            # Creating products for each category
            self.create_products(electronics, 5)
            self.create_products(clothing, 5)
            self.create_products(books, 5)

            self.stdout.write(self.style.SUCCESS('Data population complete.'))

    def create_products(self, category, num_products):
        for _ in range(num_products):
            Product.objects.create(
                name=fake.word(),
                description=fake.text(),
                price=random.uniform(10, 100),
                category=category
            )
