from django.contrib import admin
from django.urls import path
from . import views
from .views import wishlist_view, remove_from_wishlist

urlpatterns = [
    # path('admin/', admin.site.urls),
   # path('api/', include('shop.urls')),  # Add this line
    path('products/', views.get_all_products, name='get_all_products'),
    path('products/<int:pk>/', views.get_product_by_id, name='get_product_by_id'),
    path('auth/request-otp/', views.request_otp, name='request_otp'),
    path('auth/verify-otp/', views.verify_otp, name='verify_otp'),
    path('cart/add/', views.add_to_cart, name='add_to_cart'),
    # path('cart/<int:user_id>/', views.view_cart, name='view_cart'),
    path('cart/', views.view_cart, name='view_cart'),
    path('cart/update/', views.update_cart_quantity, name='update_cart_quantity'),
    path('products/add/', views.add_product, name='add_product'),
    path('cart/remove/', views.remove_from_cart, name='remove_from_cart'),
    path('order/place/', views.place_order, name='place_order'),
    # path('orders/<int:user_id>/', views.get_user_orders, name='get_user_orders'),
    path('orders/', views.get_user_orders, name='get_user_orders'),
    path('order/cancel/', views.cancel_order, name='cancel_order'),
    path('products/most-bought/', views.most_bought_products, name='most_bought_products'),
    path('products/search/', views.search_products, name='search_products'),
    # path('wishlist/', wishlist_view),
    # path('wishlist/<int:product_id>/', remove_from_wishlist),
    path('wishlist/', views.wishlist_view, name='wishlist'),
    path('wishlist/<int:product_id>/', views.remove_from_wishlist, name='remove_from_wishlist'),
    


]
