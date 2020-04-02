from django.urls import path, include

from . import views

app_name = "cafe"

urlpatterns = [
    path('baristas/', views.baristas, name='baristas'),
    path('products/', views.products, name='products'),
    path('dishes/', views.dishes, name='dishes'),
    path('<int:barista_ipn>', views.barista_detail, name='barista_detail'),
    path('', views.index, name='index'),
    path('<int:dish_id>', views.dish_detail, name='dish_detail'),
    path('food/', views.food, name='foods'),
    path('drinks/', views.drinks, name='drinks'),
    path('products/<int:product_id>', views.product_detail, name='product_detail'),
    path('login/', views.login, name='login')

]
