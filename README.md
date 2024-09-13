# Django REST E-commerce Project

This project is a Django-based RESTful API for an e-commerce platform. It provides endpoints for user management, product management, and shopping cart functionality.

## Project Structure

```
├── apps
│   ├── shop
│   ├── user
│   └── utils
├── configs
├── ops
├── tests
├── docker-compose.yml
├── manage.py
├── moc.py
├── README.md
└── requirements.txt
```

## Features

- User Authentication (Registration, Login, OTP Verification)
- Product Management (CRUD operations)
- Shopping Cart Functionality
- Order Management
- Admin Panel for Product and Category Management

## Setup

1. Clone the repository:
   ```
   git clone <repository-url>
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Set up the database:
   ```
   python manage.py migrate
   ```

4. Create a superuser:
   ```
   python manage.py createsuperuser
   ```

5. Run the development server:
   ```
   python manage.py runserver
   ```

## Authentication

The project uses token-based authentication. Include the token in the Authorization header for protected endpoints:

```
Authorization: Token <your-token>
```
## Run test
The project use standard django TestCase class. To run tests:
```
python manage.py test apps.shop.tests 
python manage.py test apps.user.tests 
```

## Rate Limiting

Rate limiting is implemented for both anonymous and authenticated users to prevent abuse of the API.

## License

This project is licensed under the MIT License
