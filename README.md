# 🛒 E-Commerce Backend API

This is a Django-based e-commerce backend supporting user authentication via mobile OTP (2Factor.in), JWT-based route protection, cart and wishlist functionality, product reviews, order placement, and payment integration-ready structure.

Hosted at:  
👉 **https://aayushchoudhary.pythonanywhere.com/**

---

## ✅ Features

- 🔐 Mobile OTP-based login using 2Factor.in
- 🔑 JWT token authentication and route protection
- 🛍️ Product listing with search, filtering, and image upload
- 🛒 Cart management with total amount calculation
- ❤️ Wishlist support
- 📦 Order placement, viewing, and cancellation
- 🧾 Order history for logged-in users
- 🔍 Most-bought product analytics
- 🌐 Public API hosted on PythonAnywhere

---

## 🚀 Tech Stack

**Backend:**  
- Python  
- Django  
- Django REST Framework  

**Authentication & Security:**  
- JWT (JSON Web Tokens)  
- Custom `@jwt_required` decorator  
- OTP via [2Factor.in](https://2factor.in/) (Voice Call API)

**Database:**  
- SQLite (default, replaceable with PostgreSQL/MySQL)

**Hosting:**  
- PythonAnywhere (Free Tier)

---

## 🧰 Python Libraries Used

- `djangorestframework` – for building RESTful APIs  
- `PyJWT` – to create and verify JWT tokens  
- `requests` – for calling 2Factor OTP API  
- `Pillow` – to handle image uploads  
- `python-dotenv` – for environment variable handling  
- `django-cors-headers` – to allow frontend requests (CORS)

---

## 📡 API Endpoints

All routes are prefixed with:  
📍 **`https://aayushchoudhary.pythonanywhere.com/api/`**

| Method | Route | Description |
|--------|-------|-------------|
| `GET` | `/products/` | List all products with optional filters |
| `GET` | `/products/<id>/` | Get details of a single product |
| `POST` | `/products/add/` | Add a new product (with image) |
| `GET` | `/products/search/?q=` | Search products by query |
| `GET` | `/products/most-bought/` | Show most bought products |
| `POST` | `/auth/request-otp/` | Send OTP to user's phone |
| `POST` | `/auth/verify-otp/` | Verify OTP and return JWT |
| `GET` | `/cart/` | View current cart items |
| `POST` | `/cart/add/` | Add product to cart |
| `POST` | `/cart/update/` | Update quantity of a cart item |
| `POST` | `/cart/remove/` | Remove item from cart |
| `POST` | `/order/place/` | Place a new order |
| `GET` | `/orders/` | View user's order history |
| `POST` | `/order/cancel/` | Cancel an order |
| `GET` | `/wishlist/` | View wishlist |
| `POST` | `/wishlist/` | Add to wishlist |
| `DELETE` | `/wishlist/<product_id>/` | Remove from wishlist |

## 🔐 Protected Routes

The following endpoints **require** JWT token:

- GET /cart/
- POST /cart/add/, /cart/update/, /cart/remove/
- POST /order/place/, POST /order/cancel/, GET /orders/
- GET /wishlist/, POST /wishlist/, DELETE /wishlist/<product_id>/

📌 **All secured routes require JWT token.**  
Example:  
`GET /products/` →  
👉 `https://aayushchoudhary.pythonanywhere.com/api/products/`

---

## 🔐 Authentication

### 🔑 Login Flow (OTP + JWT)

- User submits mobile number via `/auth/request-otp/`
- OTP is sent via voice call using 2Factor.in
- User submits received OTP to `/auth/verify-otp/`
- On successful verification:
  - A **JWT token** is returned
  - User is auto-created if they don’t exist

### 🔐 JWT Token Usage

Include JWT in headers for secured routes:

Authorization: Bearer <your_token_here>


## 🧾 API Documentation

🔗 Link to full API documentation: "https://documenter.getpostman.com/view/39033838/2sB2cbayXV"

## 📤 Image Uploads

- Product images are uploaded using `ImageField`
- Handled using `MultiPartParser` and `FormParser`
- Images served from `/media/` directory

Example payload for product creation:
```json
{
  "name": "Smartphone",
  "description": "Latest Android device",
  "price": 19999,
  "category": "mobile",
  "image": "(upload as multipart/form-data)"
}
