from django.contrib.auth import authenticate, login, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from .forms import LoginForm, RegisterForm, UserChangeForm
from django.contrib.auth import authenticate, login, get_user_model, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required


# Create your views here.
# def login_page(request):
#     context={
#         'msg': 'it is login page'
#     }
#     return render(request, 'account/login.html', context)


class UserLogin(View):

    def get(self, request):
        if request.user.is_authenticated:
            return redirect("/")
        form = LoginForm()
        context = {
            'form': form
        }
        return render(request, "account/login.html", context)

    def post(self, request):
        if request.user.is_authenticated:
            return redirect("/")
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['username'], password=cd['password'])
            if user is not None:
                login(request, user)
                return redirect("/")
            else:
                form.add_error("username", "invalid username")

                context = {
                    'form': form
                }

        return render(request, "account/login.html", context)


User = get_user_model()


def register_page(request):
    register_form = RegisterForm(request.POST or None)
    if request.user.is_authenticated:
        return redirect("/")
    if register_form.is_valid():
        userName = register_form.cleaned_data.get('userName')
        email = register_form.cleaned_data.get('email') or None
        password = register_form.cleaned_data.get('password')
        new_user = User.objects.create_user(username=userName, email=email, password=password)
        login(request, new_user)
        return redirect('/')
        # print(new_user)

    context = {
        'register_form': register_form
    }
    return render(request, 'account/register.html', context)


def log_out(request):
    logout(request)
    return redirect('/')


@login_required
def profile(request):
    user = request.user

    context = {
        'user': user
    }
    return render(request, 'account/profile.html', context)

@login_required
def edit_profile(request):
    user = request.user
    if request.method == "POST":
        form = UserChangeForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            user = form.save()
            # برای اینکه بعد از تغییر پسورد، سشن کاربر باطل نشه:
            if form.cleaned_data.get("password1"):
                update_session_auth_hash(request, user)
            return redirect("account:edit")
    else:
        form = UserChangeForm(instance=user)

    return render(request, "account/edit_profile.html", {"form": form})
