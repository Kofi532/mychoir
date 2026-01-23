from django.urls import path
from . import views

# app_name = 'school_app'

urlpatterns = [
    path('', views.home, name='home'),
    # path('academics/', views.academics, name='academics'),
    # path('news/', views.news_list, name='news_list'),
    # path('contact/', views.contact, name='contact'),

]


