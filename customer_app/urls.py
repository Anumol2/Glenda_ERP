from django.urls import path
from customer_app import views

urlpatterns = [
    path('register/',views.register, name='register'),

    path('view_customeruser',views.view_customeruser, name='view_customeruser'),
    path('customer_search',views.customer_search,name='customer_search'),
    path('view_customer_profile/<int:id>', views.view_customer_profile, name='view_customer_profile'),
    path('customer_exportsearch', views.customer_exportsearch, name='customer_exportsearch'),


]