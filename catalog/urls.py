# catalog/urls.py
from django.conf import settings
from django.conf.urls.static import static
from django.views.decorators.cache import cache_page
from django.urls import path
from .views import (
    HomeView,
    ContactsView,
    SubmitFeedbackView,
    ProductDetailView,
    CreateProductView,
    ProductListView,
    EditProductView,
    DeleteProductView,
    AddVersionView,
)

app_name = 'catalog'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('contacts/', ContactsView.as_view(), name='contacts'),
    path('contacts/submit/', SubmitFeedbackView.as_view(), name='submit_feedback'),
    path('create_product/', CreateProductView.as_view(), name='create_product'),
    path('products/', ProductListView.as_view(), name='product_list'),
    path('product/<int:product_id>/', cache_page(60 * 15)(ProductDetailView.as_view()), name='product_detail'),
    path('product/<int:product_id>/edit/', EditProductView.as_view(), name='edit_product'),
    path('product/<int:product_id>/delete/', DeleteProductView.as_view(), name='delete_product'),
    path('add_version/', AddVersionView.as_view(), name='add_version'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
