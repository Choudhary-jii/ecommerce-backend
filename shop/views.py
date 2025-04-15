# # from django.shortcuts import render

# # Create your views here.

# from rest_framework.decorators import api_view
# from rest_framework.response import Response
# from rest_framework import status
# from .models import Product
# from .serializers import ProductSerializer
# from django.db.models import Q

# import random
# import requests
# from .models import OTP

# # FAST2SMS_API_KEY = 'BaUEAkMnKO03LYPXzwdSD5obHrNCeJtmg9Vfhvsy2iIj8u4GQ1QFMZ7eY62XRjxHiO8h5AmgpIydUCw3'
# from decouple import config
# # FAST2SMS_API_KEY = config("FAST2SMS_API_KEY")
# TWOFACTOR_API_KEY = config("TWOFACTOR_API_KEY")


# @api_view(['GET'])
# def get_all_products(request):
#     # products = Product.objects.all()
#     # serializer = ProductSerializer(products, many=True)
#     # return Response(serializer.data)


#     queryset = Product.objects.all()

#     # --- Filtering ---
#     category = request.GET.get('category')
#     sold = request.GET.get('sold')
#     min_price = request.GET.get('min_price')
#     max_price = request.GET.get('max_price')
#     search = request.GET.get('search')

#     if category:
#         queryset = queryset.filter(category__iexact=category)

#     if sold in ['true', 'false']:
#         queryset = queryset.filter(sold=(sold == 'true'))

#     if min_price:
#         queryset = queryset.filter(price__gte=float(min_price))
#     if max_price:
#         queryset = queryset.filter(price__lte=float(max_price))

#     if search:
#         queryset = queryset.filter(title__icontains=search)

#     serializer = ProductSerializer(queryset, many=True)
#     return Response(serializer.data)

# @api_view(['GET'])
# def get_product_by_id(request, pk):
#     try:
#         product = Product.objects.get(pk=pk)
#         serializer = ProductSerializer(product)
#         return Response(serializer.data)
#     except Product.DoesNotExist:
#         return Response({'error': 'Product not found'}, status=404)


# # def send_otp_sms(mobile, otp):
# #     url = "https://www.fast2sms.com/dev/bulkV2"
# #     headers = {
# #         "authorization": FAST2SMS_API_KEY
# #     }
# #     payload = {
# #         "variables_values": otp,
# #         "route": "otp",
# #         "numbers": mobile
# #     }

# #     response = requests.post(url, headers=headers, data=payload)
# #     return response.json()


# def send_otp_sms(mobile):
#     template_name = "SMS_OTP_LOGIN"  # change this if you named it differently
#     url = f"https://2factor.in/API/V1/{TWOFACTOR_API_KEY}/SMS/+91{mobile}/AUTOGEN/{template_name}"
#     response = requests.get(url)
#     return response.json()


# @api_view(['POST'])
# def request_otp(request):
#     mobile = request.data.get('mobile')
#     if not mobile:
#         return Response({'error': 'Mobile number required'}, status=400)

#     sms_result = send_otp_sms(mobile)

#     if sms_result.get('Status') == 'Success':
#         session_id = sms_result.get('Details')
#         OTP.objects.create(mobile=mobile, session_id=session_id)
#         return Response({'message': 'OTP sent to mobile'})

#     return Response({'error': 'Failed to send OTP', 'api_response': sms_result}, status=400)




# from .models import User, OTP
# from rest_framework.response import Response
# from rest_framework.decorators import api_view

# # @api_view(['POST'])
# # def verify_otp(request):
# #     mobile = request.data.get('mobile')
# #     otp_input = request.data.get('otp')

# #     try:
# #         otp_entry = OTP.objects.filter(mobile=mobile).latest('created_at')
# #         session_id = otp_entry.session_id
# #     except OTP.DoesNotExist:
# #         return Response({'error': 'OTP session not found'}, status=400)

# #     verify_url = f"https://2factor.in/API/V1/{TWOFACTOR_API_KEY}/SMS/VERIFY/{session_id}/{otp_input}"
# #     response = requests.get(verify_url).json()

# #     if response.get('Status') == 'Success':
# #         user, created = User.objects.get_or_create(
# #             mobile=mobile,
# #             defaults={'full_name': 'Guest'}
# #         )
# #         return Response({
# #             'message': 'Login successful',
# #             'user_id': user.id,
# #             'full_name': user.full_name,
# #             'mobile': user.mobile,
# #             'new_user': created
# #         })

# #     return Response({'error': 'Invalid OTP'}, status=401)

# @api_view(['POST'])
# def verify_otp(request):
#     mobile = request.data.get('mobile')
#     otp_input = request.data.get('otp')
#     full_name = request.data.get('full_name', 'Guest')  # fallback to Guest

#     try:
#         otp_entry = OTP.objects.filter(mobile=mobile).latest('created_at')
#         session_id = otp_entry.session_id
#     except OTP.DoesNotExist:
#         return Response({'error': 'OTP session not found'}, status=400)

#     verify_url = f"https://2factor.in/API/V1/{TWOFACTOR_API_KEY}/SMS/VERIFY/{session_id}/{otp_input}"
#     response = requests.get(verify_url).json()

#     if response.get('Status') == 'Success':
#         user, created = User.objects.get_or_create(
#             mobile=mobile,
#             defaults={'full_name': full_name}
#         )

#         return Response({
#             'message': 'Login successful',
#             'user_id': user.id,
#             'full_name': user.full_name,
#             'mobile': user.mobile,
#             'new_user': created
#         })

#     return Response({'error': 'Invalid OTP'}, status=401)



# from .models import Cart, Product, User
# from rest_framework.decorators import api_view
# from rest_framework.response import Response

# @api_view(['POST'])
# def add_to_cart(request):
#     user_id = request.data.get('user_id')
#     product_id = request.data.get('product_id')
#     quantity = int(request.data.get('quantity', 1))

#     if not user_id or not product_id:
#         return Response({'error': 'user_id and product_id are required'}, status=400)

#     try:
#         user = User.objects.get(id=user_id)
#         product = Product.objects.get(id=product_id)
#     except User.DoesNotExist:
#         return Response({'error': 'Invalid user'}, status=404)
#     except Product.DoesNotExist:
#         return Response({'error': 'Invalid product'}, status=404)

#     cart_item, created = Cart.objects.get_or_create(user=user, product=product)
#     if not created:
#         cart_item.quantity += quantity
#     else:
#         cart_item.quantity = quantity

#     cart_item.save()

#     return Response({'message': 'Product added to cart', 'quantity': cart_item.quantity})


# # -- VIEW CART --
# @api_view(['GET'])
# def view_cart(request, user_id):
#     try:
#         user = User.objects.get(id=user_id)
#     except User.DoesNotExist:
#         return Response({'error': 'Invalid user'}, status=404)

#     cart_items = Cart.objects.filter(user=user)
#     response_data = []

#     for item in cart_items:
#         product_data = ProductSerializer(item.product).data
#         response_data.append({
#             'product': product_data,
#             'quantity': item.quantity,
#             'subtotal': item.quantity * item.product.price
#         })

#     return Response(response_data)


# # -- UPDATE QUNATITY IN CART --
# @api_view(['POST'])
# def update_cart_quantity(request):
#     user_id = request.data.get('user_id')
#     product_id = request.data.get('product_id')
#     quantity = int(request.data.get('quantity', 1))

#     try:
#         user = User.objects.get(id=user_id)
#         product = Product.objects.get(id=product_id)
#         cart_item = Cart.objects.get(user=user, product=product)
#     except (User.DoesNotExist, Product.DoesNotExist, Cart.DoesNotExist):
#         return Response({'error': 'User, product, or cart item not found'}, status=404)

#     if quantity <= 0:
#         cart_item.delete()
#         return Response({'message': 'Item removed from cart because quantity was 0 or less'})
    
#     cart_item.quantity = quantity
#     cart_item.save()

#     return Response({'message': 'Cart updated', 'quantity': cart_item.quantity})


# # -- ADD A PRODUCT --
# @api_view(['POST'])
# def add_product(request):
#     serializer = ProductSerializer(data=request.data)
#     if serializer.is_valid():
#         serializer.save()
#         return Response({'message': 'Product created successfully', 'product': serializer.data})
#     return Response(serializer.errors, status=400)


# # --Remove a product from a user's cart--
# @api_view(['POST'])
# def remove_from_cart(request):
#     user_id = request.data.get('user_id')
#     product_id = request.data.get('product_id')

#     try:
#         user = User.objects.get(id=user_id)
#         product = Product.objects.get(id=product_id)
#         cart_item = Cart.objects.get(user=user, product=product)
#     except (User.DoesNotExist, Product.DoesNotExist, Cart.DoesNotExist):
#         return Response({'error': 'User, product, or cart item not found'}, status=404)

#     cart_item.delete()
#     return Response({'message': 'Item removed from cart'})

# # --Place Order API--
# from datetime import datetime
# from .models import Order

# @api_view(['POST'])
# def place_order(request):
#     user_id = request.data.get('user_id')

#     try:
#         user = User.objects.get(id=user_id)
#     except User.DoesNotExist:
#         return Response({'error': 'Invalid user'}, status=404)

#     cart_items = Cart.objects.filter(user=user)
#     if not cart_items.exists():
#         return Response({'error': 'Cart is empty'}, status=400)

#     payment_mode = request.data.get('payment_mode', 'COD')

#     orders_created = []
#     for item in cart_items:
#         order = Order.objects.create(
#             user=user,
#             product=item.product,
#             quantity=item.quantity,
#             price=item.product.price,
#             payment_mode=payment_mode
#         )
#         orders_created.append({
#             'order_id': order.id,
#             'product': item.product.title,
#             'quantity': item.quantity
#         })
#         item.delete()  # Clear from cart

#     return Response({
#         'message': 'Order placed successfully',
#         'orders': orders_created
#     })


# # --Get All Orders for a User--
# @api_view(['GET'])
# def get_user_orders(request, user_id):
#     try:
#         user = User.objects.get(id=user_id)
#     except User.DoesNotExist:
#         return Response({'error': 'Invalid user'}, status=404)

#     # orders = Order.objects.filter(user=user).order_by('-date')
#     orders = Order.objects.filter(user=user).order_by('-created_at')

#     data = []

#     for order in orders:
#         data.append({
#             'order_id': order.id,
#             'product': order.product.title,
#             'quantity': order.quantity,
#             'price': order.price,
#             # 'date': order.date.strftime("%Y-%m-%d %H:%M:%S")
#             'date': order.created_at.strftime("%Y-%m-%d %H:%M:%S")

#         })

#     return Response(data)


# # --Cancel Order API--
# @api_view(['POST'])
# def cancel_order(request):
#     order_id = request.data.get('order_id')

#     try:
#         order = Order.objects.get(id=order_id)
#     except Order.DoesNotExist:
#         return Response({'error': 'Order not found'}, status=404)

#     order.delete()
#     return Response({'message': f'Order {order_id} has been cancelled'})




from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q
from django.conf import settings
from .models import Product, OTP, User, Cart, Order
from .serializers import ProductSerializer
import requests, jwt, datetime

from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import BaseAuthentication

# --- JWT HELPER FUNCTIONS ---
def generate_jwt(user_id):
    payload = {
        'user_id': user_id,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=settings.JWT_EXP_DELTA_SECONDS),
        'iat': datetime.datetime.utcnow(),
    }
    token = jwt.encode(payload, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
    return token

def decode_jwt(token):
    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        return payload['user_id']
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None


# --- SEND OTP ---
TWOFACTOR_API_KEY = settings.TWOFACTOR_API_KEY

def send_otp_sms(mobile):
    template_name = "SMS_OTP_LOGIN"
    url = f"https://2factor.in/API/V1/{TWOFACTOR_API_KEY}/SMS/+91{mobile}/AUTOGEN/{template_name}"
    response = requests.get(url)
    return response.json()


# --- REQUEST OTP ---
@api_view(['POST'])
def request_otp(request):
    mobile = request.data.get('mobile')
    if not mobile:
        return Response({'error': 'Mobile number required'}, status=400)

    sms_result = send_otp_sms(mobile)
    if sms_result.get('Status') == 'Success':
        session_id = sms_result.get('Details')
        OTP.objects.create(mobile=mobile, session_id=session_id)
        return Response({'message': 'OTP sent to mobile'})

    return Response({'error': 'Failed to send OTP', 'api_response': sms_result}, status=400)


# --- VERIFY OTP & RETURN JWT TOKEN ---
@api_view(['POST'])
def verify_otp(request):
    mobile = request.data.get('mobile')
    otp_input = request.data.get('otp')
    full_name = request.data.get('full_name', 'Guest')

    try:
        otp_entry = OTP.objects.filter(mobile=mobile).latest('created_at')
    except OTP.DoesNotExist:
        return Response({'error': 'OTP session not found'}, status=400)

    session_id = otp_entry.session_id
    verify_url = f"https://2factor.in/API/V1/{TWOFACTOR_API_KEY}/SMS/VERIFY/{session_id}/{otp_input}"
    response = requests.get(verify_url).json()

    if response.get('Status') == 'Success':
        user, created = User.objects.get_or_create(mobile=mobile, defaults={'full_name': full_name})
        token = generate_jwt(user.id)
        return Response({
            'message': 'Login successful',
            'token': token,
            'full_name': user.full_name,
            'new_user': created
        })

    return Response({'error': 'Invalid OTP'}, status=401)


# --- CUSTOM DECORATOR TO EXTRACT USER ID FROM JWT ---
# def jwt_required(func):
#     def wrapper(request, *args, **kwargs):
#         auth_header = request.headers.get('Authorization')
#         if not auth_header or not auth_header.startswith('Bearer '):
#             return Response({'error': 'Authorization token missing'}, status=401)
#         token = auth_header.split(' ')[1]
#         user_id = decode_jwt(token)
#         if not user_id:
#             return Response({'error': 'Invalid or expired token'}, status=401)
#         request.user_id = user_id
#         return func(request, *args, **kwargs)
#     return wrapper
def jwt_required(func):
    def wrapper(request, *args, **kwargs):
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return Response({'error': 'Authorization token missing'}, status=401)
        
        token = auth_header.split(' ')[1]
        user_id = decode_jwt(token)
        
        if not user_id:
            return Response({'error': 'Invalid or expired token'}, status=401)
        
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=404)
        
        request.user_id = user_id
        request.user = user
        return func(request, *args, **kwargs)
    return wrapper



# ------------------- SECURED ROUTES -------------------

@api_view(['POST'])
@jwt_required
def add_to_cart(request):
    product_id = request.data.get('product_id')
    quantity = int(request.data.get('quantity', 1))
    user_id = request.user_id

    try:
        user = User.objects.get(id=user_id)
        product = Product.objects.get(id=product_id)
    except (User.DoesNotExist, Product.DoesNotExist):
        return Response({'error': 'User or product not found'}, status=404)

    cart_item, created = Cart.objects.get_or_create(user=user, product=product)
    if not created:
        cart_item.quantity += quantity
    else:
        cart_item.quantity = quantity
    cart_item.save()

    return Response({'message': 'Product added to cart', 'quantity': cart_item.quantity})


@api_view(['GET'])
@jwt_required
# def view_cart(request):
#     user_id = request.user_id
#     user = User.objects.get(id=user_id)
#     cart_items = Cart.objects.filter(user=user)
#     response_data = []
#     total_amount = 0

#     for item in cart_items:
#         product_data = ProductSerializer(item.product).data
        
#         response_data.append({
#             'product': product_data,
#             'quantity': item.quantity,
#             'subtotal': item.quantity * item.product.price
#         })

#     return Response(response_data)
def view_cart(request):
    user_id = request.user_id
    user = User.objects.get(id=user_id)
    cart_items = Cart.objects.filter(user=user)

    response_data = []
    total_amount = 0

    for item in cart_items:
        product_data = ProductSerializer(item.product).data
        subtotal = item.quantity * item.product.price
        total_amount += subtotal
        response_data.append({
            'product': product_data,
            'quantity': item.quantity,
            'subtotal': subtotal
        })

    return Response({
        'cart_items': response_data,
        'total_amount': total_amount
    })


@api_view(['POST'])
@jwt_required
def update_cart_quantity(request):
    product_id = request.data.get('product_id')
    quantity = int(request.data.get('quantity', 1))
    user_id = request.user_id

    try:
        user = User.objects.get(id=user_id)
        product = Product.objects.get(id=product_id)
        cart_item = Cart.objects.get(user=user, product=product)
    except (User.DoesNotExist, Product.DoesNotExist, Cart.DoesNotExist):
        return Response({'error': 'Item not found'}, status=404)

    if quantity <= 0:
        cart_item.delete()
        return Response({'message': 'Item removed from cart'})
    
    cart_item.quantity = quantity
    cart_item.save()
    return Response({'message': 'Cart updated', 'quantity': cart_item.quantity})


@api_view(['POST'])
@jwt_required
def remove_from_cart(request):
    product_id = request.data.get('product_id')
    user_id = request.user_id

    try:
        user = User.objects.get(id=user_id)
        product = Product.objects.get(id=product_id)
        cart_item = Cart.objects.get(user=user, product=product)
    except (User.DoesNotExist, Product.DoesNotExist, Cart.DoesNotExist):
        return Response({'error': 'Item not found'}, status=404)

    cart_item.delete()
    return Response({'message': 'Item removed from cart'})


# @api_view(['POST'])
# @jwt_required
# def place_order(request):
#     user_id = request.user_id
#     payment_mode = request.data.get('payment_mode', 'COD')

#     try:
#         user = User.objects.get(id=user_id)
#         cart_items = Cart.objects.filter(user=user)
#         if not cart_items.exists():
#             return Response({'error': 'Cart is empty'}, status=400)
#     except User.DoesNotExist:
#         return Response({'error': 'User not found'}, status=404)

#     orders_created = []
#     for item in cart_items:
#         order = Order.objects.create(
#             user=user,
#             product=item.product,
#             quantity=item.quantity,
#             price=item.product.price,
#             payment_mode=payment_mode
#         )
#         orders_created.append({
#             'order_id': order.id,
#             'product': item.product.title,
#             'quantity': item.quantity
#         })
#         item.delete()

#     return Response({'message': 'Order placed', 'orders': orders_created})
@api_view(['POST'])
@jwt_required
def place_order(request):
    user_id = request.user_id
    payment_mode = request.data.get('payment_mode', 'COD')

    try:
        user = User.objects.get(id=user_id)
        cart_items = Cart.objects.filter(user=user)
        if not cart_items.exists():
            return Response({'error': 'Cart is empty'}, status=400)
    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=404)

    orders_created = []
    total_amount = 0

    for item in cart_items:
        item_total = item.product.price * item.quantity
        total_amount += item_total

        order = Order.objects.create(
            user=user,
            product=item.product,
            quantity=item.quantity,
            price=item_total,
            payment_mode=payment_mode
        )

        orders_created.append({
            'order_id': order.id,
            'product': item.product.title,
            'quantity': item.quantity
        })

        item.delete()

    return Response({
        'message': 'Order placed',
        'orders': orders_created,
        'total_amount': total_amount
    })


@api_view(['GET'])
@jwt_required
def get_user_orders(request):
    user_id = request.user_id
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=404)

    # orders = Order.objects.filter(user=user).order_by('-created_at')
    orders = Order.objects.filter(user=user).select_related('product').order_by('-created_at')

    data = [
        {
            'order_id': order.id,
            'product': order.product.title,
            'quantity': order.quantity,
            'price': order.price,
            'date': order.created_at.strftime("%Y-%m-%d %H:%M:%S")
        }
        for order in orders
    ]
    return Response(data)


@api_view(['POST'])
@jwt_required
def cancel_order(request):
    order_id = request.data.get('order_id')
    user_id = request.user_id

    try:
        order = Order.objects.get(id=order_id, user_id=user_id)
    except Order.DoesNotExist:
        return Response({'error': 'Order not found'}, status=404)

    order.delete()
    return Response({'message': f'Order {order_id} cancelled'})


@api_view(['GET'])
def get_all_products(request):
    # products = Product.objects.all()
    # serializer = ProductSerializer(products, many=True)
    # return Response(serializer.data)


    queryset = Product.objects.all()

    # --- Filtering ---
    category = request.GET.get('category')
    sold = request.GET.get('sold')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    search = request.GET.get('search')

    if category:
        queryset = queryset.filter(category__iexact=category)

    if sold in ['true', 'false']:
        queryset = queryset.filter(sold=(sold == 'true'))

    if min_price:
        queryset = queryset.filter(price__gte=float(min_price))
    if max_price:
        queryset = queryset.filter(price__lte=float(max_price))

    if search:
        queryset = queryset.filter(title__icontains=search)

    serializer = ProductSerializer(queryset, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def get_product_by_id(request, pk):
    try:
        product = Product.objects.get(pk=pk)
        serializer = ProductSerializer(product)
        return Response(serializer.data)
    except Product.DoesNotExist:
        return Response({'error': 'Product not found'}, status=404)


# -- ADD A PRODUCT --
# @api_view(['POST'])
# def add_product(request):
#     serializer = ProductSerializer(data=request.data)
#     if serializer.is_valid():
#         serializer.save()
#         return Response({'message': 'Product created successfully', 'product': serializer.data})
#     return Response(serializer.errors, status=400)
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.decorators import parser_classes


@api_view(['POST'])
@parser_classes([MultiPartParser, FormParser])
def add_product(request):
    serializer = ProductSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({'message': 'Product added successfully', 'product': serializer.data})
    return Response(serializer.errors, status=400)


from django.db.models import Sum
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Order, Product
from .serializers import ProductSerializer

@api_view(['GET'])
def most_bought_products(request):
    top_products = (
        Order.objects
        .values('product')
        .annotate(total_sold=Sum('quantity'))
        .order_by('-total_sold')[:10]  # top 10
    )

    product_ids = [item['product'] for item in top_products]
    products = Product.objects.filter(id__in=product_ids)
    serialized = ProductSerializer(products, many=True).data

    # Optional: Add `total_sold` info to each product
    product_map = {item['product']: item['total_sold'] for item in top_products}
    for product in serialized:
        product['total_sold'] = product_map[product['id']]

    return Response(serialized)

from django.db.models import Q
from django.http import JsonResponse
from .models import Product
from .serializers import ProductSerializer

# def search_products(request):
#     query = request.GET.get('query', '')
#     price_lt = request.GET.get('price_lt')
#     price_gt = request.GET.get('price_gt')

#     products = Product.objects.all()

#     if query:
#         products = products.filter(
#             Q(title__icontains=query) |
#             Q(description__icontains=query) |
#             Q(category__icontains=query)
#         )

#     if price_lt:
#         products = products.filter(price__lt=price_lt)
#     if price_gt:
#         products = products.filter(price__gt=price_gt)

#     serializer = ProductSerializer(products, many=True)
#     return JsonResponse(serializer.data, safe=False)


@api_view(['GET'])
def search_products(request):
    query = request.GET.get('query', '')
    max_price = request.GET.get('max_price')

    if query:
        products = Product.objects.filter(
            Q(title__icontains=query) | Q(description__icontains=query) | Q(category__icontains=query)
        )
    else:
        products = Product.objects.all()

    if max_price:
        try:
            max_price = float(max_price)
            products = products.filter(price__lte=max_price)
        except ValueError:
            pass  # Ignore invalid max_price values

    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)


# ---WISHLIST---
from .models import Wishlist
from .serializers import WishlistSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status


# @api_view(['GET', 'POST'])
# @jwt_required
# def wishlist_view(request):
#     user = request.user

#     if request.method == 'GET':
#         items = Wishlist.objects.filter(user=user)
#         serializer = WishlistSerializer(items, many=True)
#         return Response(serializer.data)

#     elif request.method == 'POST':
#         product_id = request.data.get('product_id')
#         if not product_id:
#             return Response({'error': 'Product ID required'}, status=400)

#         if Wishlist.objects.filter(user=user, product_id=product_id).exists():
#             return Response({'message': 'Already in wishlist'}, status=200)

#         Wishlist.objects.create(user=user, product_id=product_id)
#         return Response({'message': 'Added to wishlist'}, status=201)
@api_view(['GET', 'POST'])
@jwt_required
def wishlist_view(request):
    user = request.user
    print("Authenticated user:", user)

    if request.method == 'GET':
        items = Wishlist.objects.filter(user=user)
        print("Wishlist items:", items)
        serializer = WishlistSerializer(items, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        product_id = request.data.get('product_id')
        print("Product ID received:", product_id)

        if not product_id:
            return Response({'error': 'Product ID required'}, status=400)

        if Wishlist.objects.filter(user=user, product_id=product_id).exists():
            print("Already in wishlist")
            return Response({'message': 'Already in wishlist'}, status=200)

        Wishlist.objects.create(user=user, product_id=product_id)
        print("Added to wishlist")
        return Response({'message': 'Added to wishlist'}, status=201)


@api_view(['DELETE'])
@jwt_required
def remove_from_wishlist(request, product_id):
    user = request.user
    try:
        item = Wishlist.objects.get(user=user, product_id=product_id)
        item.delete()
        return Response({'message': 'Removed from wishlist'})
    except Wishlist.DoesNotExist:
        return Response({'error': 'Item not in wishlist'}, status=404)
