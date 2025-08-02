from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.views import View
from .forms import LoginForm
from django.contrib.auth import authenticate, login, get_user_model, logout
from .forms import RegisterForm

# Create your views here.
# def login_page(request):
#     context={
#         'msg': 'it is login page'
#     }
#     return render(request, 'account/login.html', context)

User = get_user_model()


class UserLogin(View):

    def get(self, request):
        form = LoginForm()
        context = {
            'form': form
        }
        return render(request, "account/login.html", context)

    def post(self, request):
        form = LoginForm(request.POST)
        context = {
            'form': form
        }
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['username'], password=cd['password'])
            if user is not None:
                login(request, user)
                return redirect("/")
            else:
                form.add_error("username", "invalid username")

        return render(request, "account/login.html", context)


def register_page(request):
    register_form = RegisterForm(request.POST or None)
    if register_form.is_valid():
        userName = register_form.cleaned_data.get('userName')
        email = register_form.cleaned_data.get('email')
        password = register_form.cleaned_data.get('password')
        new_user = User.objects.create_user(username=userName, email=email, password=password)
        print(new_user)

    context = {
        'register_form': register_form
    }
    return render(request, 'account/register.html', context)


def log_out(request):
    logout(request)
    return redirect('account:login')
