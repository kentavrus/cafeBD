from django.urls import path

from . import views

app_name = "cafe"

urlpatterns = [
    path('baristas/', views.baristas, name='baristas'),
    path('<int:barista_ipn>', views.barista_detail, name='barista_detail'),
    path('', views.index, name='index'),
    path('<int:dish_id>', views.dish_detail, name='dish_detail'),
    path('dishes/', views.dishes, name='dishes'),
    path('food/', views.food, name='foods'),
    path('drinks/', views.drinks, name='drinks')
]