from django.urls import path
from .views import ProductsList, product_detail, SearchProducts, ProductsListByCategory, products_categories_partial


app_name = 'eshop_products'

urlpatterns = [
    path('products', ProductsList.as_view(), name='products_list'),
    path('products/<int:product_id>/<str:title>', product_detail, name="product_detail"),
    path('products/search', SearchProducts.as_view()),
    path('products/<category_name>', ProductsListByCategory.as_view()),
]