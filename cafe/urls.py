from django.urls import path, include

from . import views

app_name = "cafe"

urlpatterns = [
    path('owner/', views.home, name='baristas'),
    path('baristas/', views.baristas, name='baristas'),
    path('suppliers/', views.suppliers, name='suppliers'),
    path('suppliers/<int:supplier_edrpou>', views.supplier_detail, name='supplier_detail'),
    path('products/', views.products, name='products'),
    path('dishes/', views.dishes, name='dishes'),
    path('baristas/<int:barista_ipn>', views.barista_detail, name='barista_detail'),
    path('', views.index, name='index'),
    path('home/', views.home, name='home'),
    path('dishes/<int:dish_id>', views.dish_detail, name='dish_detail'),
    path('dishes/food/', views.food, name='foods'),
    path('dishes/drinks/', views.drinks, name='drinks'),
    path('products/<int:product_id>', views.product_detail, name='product_detail'),
    path('login/', views.login, name='login'),
    path('add_barist/', views.add_barist, name='add_barist'),
    path('barist_add/', views.barist_add, name='barist_add'),
    path('bills/', views.bills, name='bills'),
    path("bills/<int:bill_id>", views.bill_detail, name='bill_detail'),
    path('add_bill/', views.add_bill, name='add_bill'),
    path('bill_add/', views.bill_add, name='bill_add'),
]
