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

## 🛠️ Installation Guide

Follow these steps to set up the backend on your local machine:

1. Clone the Repository
- git clone https://github.com/your-username/your-repo-name.git
- cd your-repo-name

2. Set Up a Virtual Environment
- It’s recommended to use a virtual environment to manage dependencies.

Create virtual environment : python -m venv env

Activate virtual environment : 

- On Windows : env\Scripts\activate

 - On macOS/Linux : source env/bin/activate

3. Install Required Python Packages
   
- Install all dependencies : pip install -r requirements.txt

- If requirements.txt is not available, manually install the required packages:

1. pip install django
2. pip install djangorestframework
3. pip install djangorestframework-simplejwt
4. pip install pyjwt
5. pip install requests
6. pip install pillow
7. pip install python-dotenv
8. pip install django-cors-headers

4. Set Up Environment Variables
 **Create a .env file in the project root directory and add the following:**

- SECRET_KEY=your-django-secret-key
- DEBUG=True
- ALLOWED_HOSTS=127.0.0.1,localhost
- TWO_FACTOR_API_KEY=your-2factor-api-key

ℹ️ Notes:

- SECRET_KEY: You can generate one using Django's get_random_secret_key().
- TWO_FACTOR_API_KEY: Your API key from 2Factor.in.
  
5. Run Database Migrations
   
- Apply migrations to set up your database:

1. python manage.py makemigrations
2. python manage.py migrate

6. Create a Superuser (Optional)
   
- Create a superuser to access Django admin : python manage.py createsuperuser

7. Run the Development Server
   
- Start the Django development server : python manage.py runserver

Visit your backend at:
👉 http://127.0.0.1:8000/

## 📢 Notes

- Product images uploaded via API will be stored in the /media/ directory.
- Make sure DEBUG=True for local testing and DEBUG=False in production.
- CORS headers are configured to allow frontend communication (e.g., Vue.js frontend).

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
