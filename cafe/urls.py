from django.urls import path, include

from . import views

app_name = "cafe"

urlpatterns = [
    path('home/', views.home, name='home'),
    path('logout/', views.logout, name="logout"),
    path('baristas/', views.baristas, name='baristas'),
    path('suppliers/', views.suppliers, name='suppliers'),
    path('suppliers/<int:supplier_edrpou>', views.supplier_detail, name='supplier_detail'),
    path('products/', views.products, name='products'),
    path('dishes/', views.dishes, name='dishes'),
    path('', views.index, name='index'),
    path('home/', views.home, name='home'),
    path('dishes/food/', views.food, name='foods'),
    path('dishes/drinks/', views.drinks, name='drinks'),
    path('login/', views.login, name='login'),
    path('add_barist/', views.add_barist, name='add_barist'),
    path('barist_add/', views.barist_add, name='barist_add'),
    path('bills/', views.bills, name='bills'),
    path("bills/<int:bill_id>", views.bill_detail, name='bill_detail'),
    path('add_bill/', views.add_bill, name='add_bill'),
    path('bill_add/', views.bill_add, name='bill_add'),
    path('supplier_add/', views.supplier_add, name='supplier_add'),
    path('add_supplier/', views.add_supplier, name='add_supplier'),
    path('invoices/', views.invoices, name='invoices'),
    path('add_invoice/', views.add_invoice, name='add_invoice'),
    path('invoice_add/', views.invoice_add, name='invoice_add'),
    path('invoice_detail/<int:invoice_id>', views.invoice_detail, name='invoice_detail'),
    path('add_dish/', views.add_dish, name='add_dish'),
    path('dish_add/', views.dish_add, name='dish_add'),
    path('add_product/', views.add_product, name='add_product'),
    path('product_add/', views.product_add, name='product_add')
]
