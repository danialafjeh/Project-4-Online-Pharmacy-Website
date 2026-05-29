from django.urls import path
from main import views

urlpatterns = [
    path('', views.home, name='home'),
    path('aboutus/', views.aboutus, name='aboutus'),
    path('activesales/', views.active_sales, name='active_sales'),
    path('allproducts/', views.all_products, name='all_products'),
    path('categories/', views.category_page, name='category_page'),
    path('category_selection/<str:cat>', views.category_selection, name='category_selection'),
    path('brands/', views.brands_page, name='brands_page'),
    path('brands_selection/<str:brand>', views.brands_selection, name='brand_selection'),
    path('search/', views.search, name='search_products'),
    path('signup/', views.signup_user, name='signup_user'),
    path('login_mainpage/', views.login_mainpage, name='login_mainpage'),
    path('login_customer/', views.login_customer, name='login_customer'),
    path('login_admin/', views.login_admin, name='login_admin'),
    path('logout/', views.logout_account, name='logout_account'),
    path('profile_mainpage/', views.profile_mainpage, name='profile_mainpage'),
    path('account_info/', views.account_info, name='acc_info'),
    path('update_account_info/', views.update_account_info, name='update_acc_info'),
    path('update_account_password/', views.update_account_password, name='update_acc_password'),
    path('show_deliveryinfo/', views.show_deliveryinfo, name='show_deliveryinfo'),
    path('add_deliveryinfo/', views.add_deliveryinfo , name='add_deliveryinfo'),
    path('product_details/<int:pk>', views.product_details, name='prod_details')
    
]