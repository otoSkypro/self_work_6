from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import (
    HomeView,
    ContactsView,
    SubmitFeedbackView,
    ProductDetailView,
    CreateProductView,
    ProductListView,
)

app_name = 'catalog'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('contacts/', ContactsView.as_view(), name='contacts'),
    path('contacts/submit/', SubmitFeedbackView.as_view(), name='submit_feedback'),
    path('product/<int:product_id>/', ProductDetailView.as_view(), name='product_detail'),
    path('create_product/', CreateProductView.as_view(), name='create_product'),
    path('products/', ProductListView.as_view(), name='product_list'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)