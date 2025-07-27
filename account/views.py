from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.views import View
from .forms import LoginForm


# Create your views here.
# def login_page(request):
#     context={
#         'msg': 'it is login page'
#     }
#     return render(request, 'account/login.html', context)


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
