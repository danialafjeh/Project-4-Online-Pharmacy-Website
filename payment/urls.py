from django.urls import path
from payment import views

urlpatterns = [
    path('create_order/', views.create_order, name='create_order'),
    path('orders_tracking/', views.orders_tracking, name='orders_tracking'),
    path('order_details/<int:pk>', views.order_details, name='order_details'),
    path('cancel_order/<int:order_id>', views.cancel_order, name='cancel_order')
]
