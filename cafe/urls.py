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
    path('product_add/', views.product_add, name='product_add'),
    path('search_bill/', views.search_bill, name='searchBill'),
    path('search_product/', views.search_product, name='search_product'),
    path('search_invoices/', views.search_invoices, name='searchInvoices'),
    path('delete_dish/<int:dish_id>', views.delete_dish, name='delete_dish'),
    path('sort_bills<int:vector>/', views.sort_bills, name='sort_bills'),
    path('sort_invoices<int:vector>/', views.sort_invoices, name='sort_invoices'),
    path('bills_with_foods_drinks/', views.bills_with_foods_drinks, name='bills_with_foods_drinks'),
    path('quantity_of_bills/', views.quantity_of_bills, name='quantity_of_bills'),
    path('get_suppliers/', views.get_suppliers, name='get_suppliers'),

]
