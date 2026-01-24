from django.urls import path
from . import views
from django.views.generic.base import TemplateView



urlpatterns = [
    path('', views.home, name='home'),
    path("google21ee13cc0126980b.html", TemplateView.as_view(template_name="google21ee13cc0126980b.html")),

]


