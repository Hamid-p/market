from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView

from .models import ContactUs

from .forms import ContactUsForm
from eshop_settings.models import Settings


# Create your views here.


# def contact_us_page(request):
#     contact_form = ContactUsForm(request.POST or None)
#     if contact_form.is_valid():
#         form_data=contact_form.cleaned_data
#         # fullName = contact_form.cleaned_data.get('fullName')
#         # email = contact_form.cleaned_data.get('email')
#         # message = contact_form.cleaned_data.get('message')
#         # new_contact = ContactUs.objects.create(fullName=fullName, email=email, message=message)
#         new_contact = ContactUs.objects.create(**form_data)
#
#
#     setting = Settings.objects.first()
#     context = {
#         'contact_form': contact_form,
#         'setting': setting
#     }
#     return render(request, 'contact_us_page.html', context)


class ContactusView(CreateView):
    model = ContactUs
    form_class = ContactUsForm
    # fields = "__all__"
    success_url = reverse_lazy('home')
    template_name = "contact_us_page.html"
