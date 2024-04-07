# catalog/admin.py
from django.contrib import admin
from .models import Category, Product


class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'category', 'publish_status', 'moderation_status')  # Добавляем столбец с статусом модерации
    list_filter = ('category', 'publish_status', 'moderation_status')  # Добавляем фильтр по статусу публикации и модерации
    search_fields = ('name', 'description')
    actions = ['make_published', 'make_draft', 'make_archived', 'approve_products', 'reject_products']

    def make_published(self, request, queryset):
        queryset.update(publish_status='published')

    def make_draft(self, request, queryset):
        queryset.update(publish_status='draft')

    def make_archived(self, request, queryset):
        queryset.update(publish_status='archived')

    def approve_products(self, request, queryset):
        queryset.update(moderation_status='approved', publish_status='published')

    def reject_products(self, request, queryset):
        queryset.update(moderation_status='rejected', publish_status='draft')

    make_published.short_description = 'Опубликовать выбранные продукты'
    make_draft.short_description = 'Перевести выбранные продукты в черновик'
    make_archived.short_description = 'Архивировать выбранные продукты'
    approve_products.short_description = 'Одобрить выбранные продукты'
    reject_products.short_description = 'Отклонить выбранные продукты'

    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']  # Убираем стандартное действие удаления
        return actions

    def save_model(self, request, obj, form, change):
        if obj.moderation_status == 'approved' and obj.publish_status != 'published':
            obj.publish_status = 'published'
        super().save_model(request, obj, form, change)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)


admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
