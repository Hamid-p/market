from eshop_products.models import Product



def recent_products(request):
    recent_products=Product.objects.order_by('-time')

    return {"recent_products": recent_products} #kelide recent_products dar hameye templatesha dar dastras ast