import itertools
from django.http import Http404
from django.shortcuts import render
from django.views.generic.list import ListView

from eshop_products_category.models import ProductCategory
from eshop_tag.models import Tag
from .models import Product, ProductGallery
from eshop_order.forms import UserNewOrderForm
from .serializers import ProductSerializer
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.views import APIView


class ProductsList(ListView):
    template_name = 'eshop_products/products_list.html'
    paginate_by = 6

    def get_queryset(self):
        return Product.objects.get_active_products()


# region api
@api_view(['GET', 'post'])
def productlist(request: Request):
    if request.method == 'GET':
        products = Product.objects.all()
        product_serializer = ProductSerializer(products, many=True)
        return Response(product_serializer.data, status.HTTP_200_OK)
    elif request.method == 'POST':
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status.HTTP_201_CREATED)
    return Response(None, status.HTTP_400_BAD_REQUEST)


class ManageProductApiView(APIView):
    def get(self, request: Request):
        products = Product.objects.all()
        product_serializer = ProductSerializer(products, many=True)
        return Response(product_serializer.data, status.HTTP_200_OK)

    def post(self, request: Request):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status.HTTP_201_CREATED)
        else:
            return Response(None, status.HTTP_400_BAD_REQUEST)


class ProductDetailApiView(APIView):
    def get_object(self, product_id: int):
        try:
            product = Product.objects.get(pk=product_id)
            return product
        except Product.DoesNotExist:
            return Response(None, status.HTTP_404_NOT_FOUND)

    def get(self, request: Request, product_id: int):
        product = self.get_object(product_id)
        serializer = ProductSerializer(product)
        return Response(serializer.data, status.HTTP_200_OK)

    def put(self, request: Request, product_id: int):
        product = self.get_object(product_id)
        serializer=ProductSerializer(product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status.HTTP_202_ACCEPTED)
        return Response(None, status.HTTP_400_BAD_REQUEST)

    def delete(self, request: Request, product_id: int):
        product = self.get_object(product_id)
        product.delete()
        return Response(None, status.HTTP_204_NO_CONTENT)

# endregion

class ProductsListByCategory(ListView):
    template_name = 'eshop_products/products_list.html'
    paginate_by = 6

    def get_queryset(self):
        category_name = self.kwargs['category_name']
        print(category_name)
        categories = ProductCategory.objects.filter(name__iexact=category_name)
        if categories is None:
            raise Http404('صفحه مورد نظر یافت نشد!')

        return Product.objects.get_product_by_category(category_name)


def products_categories_partial(request):
    categories = ProductCategory.objects.all()
    context = {
        'categories': categories
    }
    return render(request, 'eshop_products/categories_view_partial.html', context)


def list_grouper(n, iterable):
    args = [iter(iterable)] * n
    return ([e for e in t if e is not None] for t in itertools.zip_longest(*args))


def product_detail(request, *args, **kwargs):
    get_product_id = kwargs['product_id']
    new_order_form = UserNewOrderForm(request.POST or None, initial=({'product_id': get_product_id}))

    product = Product.objects.get_product_by_id(get_product_id)
    if product is None:
        raise Http404('محصول مورد نظر یافت نشد!')

    product.visits += 1
    product.save()

    gallery = ProductGallery.objects.filter(product_id=get_product_id)

    related_products = Product.objects.get_queryset().filter(categories__product=product).distinct()
    group_related_products = list(list_grouper(3, related_products))
    print(group_related_products)

    context = {
        'product': product,
        'gallery': gallery,
        'related_products': related_products,
        'group_related_products': group_related_products,
        'new_order_form': new_order_form
    }

    return render(request, 'eshop_products/product_detail.html', context)


class SearchProducts(ListView):
    template_name = 'eshop_products/products_list.html'
    paginate_by = 10  # چون در تمپلیت از page_obj(به جای object_list فک کنم) استفاده کردیم باید paginate_by را مقداردهی کنیم

    def get_queryset(self):
        query = self.request.GET.get('q')  # نام اینپوت در تمپلیت را q گذاشته ام
        print(query)
        if query is not None:
            return Product.objects.search_products(query)

        return Product.objects.get_active_products()
