from django.urls import path, include
from .views import ProductsList, product_detail, SearchProducts, \
    ProductsListByCategory, products_categories_partial, productlist, \
    ProductDetailApiView, ManageProductApiView, ProductGenericApiView, \
    ProductGenericDetailApiView, ProductViewSetApiView, CategoriesgenericApiView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('', ProductViewSetApiView)

app_name = 'eshop_products'

urlpatterns = [
    path('products/', ProductsList.as_view(), name='products_list'),
    path('products/<int:product_id>/<str:title>/', product_detail, name="product_detail"),
    path('products/search/', SearchProducts.as_view()),
    # api
    path('products/api/', productlist),
    path('products/cbv/api/<int:product_id>', ProductDetailApiView.as_view()),
    path('products/cbv/api/', ManageProductApiView.as_view()),
    path('products/generics/', ProductGenericApiView.as_view()),
    path('products/generics/<pk>/', ProductGenericDetailApiView.as_view()),
    path('products/viewsets/', include(router.urls)),
    path('products/categories/api/', CategoriesgenericApiView.as_view()),
    # end api
    path('products/<category_name>/', ProductsListByCategory.as_view()),

]
