# from django.contrib.auth import authenticate, login, get_user_model, logout
from django.shortcuts import render, redirect
from .forms import LoginForm
from eshop_sliders.models import Slider
from eshop_settings.models import Settings
from eshop_products.models import Product

def header(request):
    setting = Settings.objects.first()
    context = {
        'item2':'item2',
        'menu_item': 'منو سفارشی از رندر پارشیال',
        'setting': setting
    }
    return render(request, 'base/header.html', context)


def footer(request):
    setting = Settings.objects.first()
    context = {
        'setting': setting
    }
    return render(request, 'base/footer.html', context)


def home_page(request):
    featured_products = Product.objects.filter(featured=True)
    most_visits_products = Product.objects.order_by('-visits').all()[:5]
    latest_products = Product.objects.order_by('-id').all()[:5]
    sliders = Slider.objects.all()
    context = {
        'sliders': sliders,
        'featured_products': featured_products,
        'most_visits_products': most_visits_products,
        'latest_products': latest_products
    }
    return render(request, 'home_page.html', context)



# AUTH section
# def login_page(request):
#     login_form = LoginForm(request.POST or None)
#     if login_form.is_valid():
#         userName = login_form.cleaned_data.get('userName')
#         password = login_form.cleaned_data.get('password')
#         user = authenticate(request, username=userName, password=password)
#         if user is not None:
#             login(request, user)
#             return redirect('/profile')
#         else:
#             print('Error')
#     context = {
#         'login_form': login_form
#     }
#     return render(request, 'login.html', context)









# AUTH section
