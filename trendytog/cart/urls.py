from django.urls import include, path
from . import views

app_name = 'cart'

urlpatterns = [
    path('', views.cart_detail, name='cart_detail'),

    path('add/<int:product_id>/', views.add_cart, name='add_cart'),
    path('remove/<int:product_id>/', views.cart_remove, name='cart_remove'),
    path('full-remove/<int:product_id>/', views.full_remove, name='full_remove'),
    path('checkout/', views.checkout, name='checkout'),
    path('payment-success/', views.payment_success, name='payment_success'),
    path('start-payment/',views.start_payment,name='start_payment'),
    path('payment-success/',views.payment_success,name="payment_success"),
    
]

