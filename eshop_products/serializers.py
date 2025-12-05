from rest_framework import serializers
from .models import Product
from eshop_products_category.models import ProductCategory


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['title', 'description', 'price', 'image', 'active']


class CategoriesSerializer(serializers.ModelSerializer):
    product_set = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='title'  # نام فیلدی از مدل Product که میخواهید نمایش دهد
    )
    #product_set = ProductSerializer(read_only=True, many=True)  # product_set name rezerv shodeh ast,

    # agar dar modele product dar filde category az related_name estefadeh kardimT haman name ra be jaye product_set estefadeh mikonim
    class Meta:
        model = ProductCategory
        fields = '__all__'
