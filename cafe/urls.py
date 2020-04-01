from django.urls import path

from . import views

app_name = "cafe"

urlpatterns = [
    path('baristas/', views.baristas, name='baristas'),
    path('<int:barista_ipn>', views.barista_detail, name='barista_detail'),
    path('', views.index, name='index')
]