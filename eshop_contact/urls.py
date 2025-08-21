from django.urls import path

from eshop_contact.views import ContactusView

app_name = 'eshop_contact'

urlpatterns = [
    path('', ContactusView.as_view(), name="contact"),

]