# Django REST E-Commerce Project

This project is a Django-based REST API for an e-commerce platform. It provides endpoints for user management, product browsing, cart operations, and order processing.

## Table of Contents

- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
- [API Endpoints](#api-endpoints)
- [Testing](#testing)
- [Docker](#docker)
- [Contributing](#contributing)
- [License](#license)

## Features

- User registration and authentication with OTP verification
- Product and category management
- Shopping cart functionality
- Order placement and history
- User address management
- Product rating and commenting

## Prerequisites

- Python 3.8+
- pip
- virtualenv (recommended)
- Docker (optional)

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/M0h4mmadH/ex-online-shop
   cd ex-online-shop
   ```

2. Create and activate a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

4. Set up the database:
   ```
   python manage.py migrate
   ```

5. Create a superuser:
   ```
   python manage.py createsuperuser
   ```

## Usage

To run the development server:

```
python manage.py runserver
```

The API will be available at `http://localhost:8000/api/v1/`.

## API Endpoints

### User Management
- `POST /api/v1/register/`: User registration
- `POST /api/v1/login/`: User login
- `POST /api/v1/verify-otp/`: OTP verification

### Shop
- `GET /api/v1/products/`: List products
- `GET /api/v1/categories/`: List categories
- `POST /api/v1/products/create/`: Create a product (Admin only)
- `POST /api/v1/products/update/`: Update a product (Admin only)
- `POST /api/v1/categories/create/`: Create a category (Admin only)
- `POST /api/v1/categories/update/`: Update a category (Admin only)
- `POST /api/v1/cart/add-items/`: Add items to cart
- `POST /api/v1/cart/delete/`: Delete a cart
- `GET /api/v1/user/get-purchases/`: Get user's purchase history
- `GET /api/v1/user/get-active-carts/`: Get user's active carts
- `POST /api/v1/product/comment/`: Add a comment to a product
- `POST /api/v1/product/rate`: Rate a product
- `POST /api/v1/user/address/create`: Create a user address
- `POST /api/v1/user/address/update`: Update a user address
- `POST /api/v1/user/address/delete`: Delete a user address
- `GET /api/v1/user/address/get`: Get user addresses
- `POST /api/v1/cart/purchase`: Purchase items in a cart

For detailed information about request and response formats, please refer to the Postman API documentation.

## Run test
The project use standard django TestCase class. To run tests:
```
python manage.py test apps.shop.tests 
python manage.py test apps.user.tests 
```
## Run server
Run following command to run the project:

``python manage.py runserver ``
