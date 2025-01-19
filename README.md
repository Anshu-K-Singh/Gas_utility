# Gas Utility Service Request System

A Django REST Framework based service request management system for gas utility services.

## Features

- Customer service request submission and tracking
- Support representative dashboard
- Real-time status updates
- File upload support
- JWT Authentication
- Profile management

## Setup Instructions

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run migrations:
```bash
python manage.py makemigrations
python manage.py migrate
```

4. Create a superuser:
```bash
python manage.py createsuperuser
```

5. Run the development server:
```bash
python manage.py runserver
```

## API Documentation


# Gas Utility Service Request System - API Documentation

## 🔐 Authentication and Token Management

### Token Types
1. **Access Token**: Short-lived token for API authentication
   - Expires after 5 minutes
   - Used for making authenticated requests
2. **Refresh Token**: Long-lived token to obtain new access tokens
   - Expires after 24 hours
   - Used to generate new access tokens without re-login

### Token Usage Guide

#### 1. Obtaining Tokens
- **Endpoint**: `POST /api/v1/login/`
- **Request Body**:
```json
{
    "username": "user_identifier",
    "password": "user_password"
}
```
- **Response**:
```json
{
    "refresh": "long_refresh_token_here",
    "access": "short_lived_access_token_here"
}
```

#### 2. Using Access Token in Requests
- **Header Format**:
```
Authorization: Bearer {access_token}
```
- **Example**:
```
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
```

#### 3. Refreshing Access Token
- **Endpoint**: `POST /api/v1/login/refresh/`
- **Request Body**:
```json
{
    "refresh": "long_refresh_token_here"
}
```
- **Response**: New access token

## 🔐 User Types and Authentication

### 1. Customer Registration
- **Endpoint**: `POST /api/v1/register/`
- **User Type**: Customer
- **Purpose**: Create a new customer account for Gas Utility Services

#### Request Example (Customer)
```json
{
    "username": "anshu_singh",
    "password": "CustomerGas@2024",
    "password2": "CustomerGas@2024",
    "email": "anshu.singh@gmail.com",
    "first_name": "Anshu",
    "last_name": "Singh",
    "phone_number": "+917890123456",
    "address": "Flat 302, Sunrise Apartments, Koramangala, Bengaluru - 560095",
    "user_type": "customer"
}
```

### 2. Support Representative Registration
- **Endpoint**: `POST /api/v1/register/`
- **User Type**: Support Representative
- **Purpose**: Create a new support representative account

#### Request Example (Support Representative)
```json
{
    "username": "abhishek_support",
    "password": "SupportGas@2024",
    "password2": "SupportGas@2024",
    "email": "abhishek.support@gasutility.com",
    "first_name": "Abhishek",
    "last_name": "Singh",
    "phone_number": "+919876543210",
    "address": "Gas Utility Office, Corporate Park, Mumbai - 400001",
    "user_type": "support"
}
```

## 🔑 Authentication Workflows

### Customer Authentication
1. Login Endpoint
```json
{
    "username": "anshu_singh",
    "password": "CustomerGas@2024"
}
```

### Support Representative Authentication
1. Login Endpoint
```json
{
    "username": "abhishek_support",
    "password": "SupportGas@2024"
}
```

## 👤 Profile Management Endpoints

### 1. Customer Profile Endpoints
- **Retrieve Profile**: `GET /api/v1/profile/`
  - Returns full profile information
- **Update Profile**: `PUT /api/v1/profile/`
  - Allows updating profile details
- **Partial Update**: `PATCH /api/v1/profile/`
  - Update specific profile fields

#### Profile Update Example
```json
{
    "email": "new.anshu@gmail.com",
    "phone_number": "+918765432109",
    "address": "New Apartment, Hyderabad - 500001"
}
```

### 2. Support Representative Profile Endpoints
- Same endpoints as customer profile
- Additional restrictions based on role

## 🛠 Service Request Endpoints

### Customer-Specific Endpoints

#### 1. Create Service Request
- **Endpoint**: `POST /api/v1/requests/`
- **Permissions**: Authenticated Customers Only

##### Request Examples

1. Gas Leak Inspection
```json
{
    "request_type": "gas_leak_inspection",
    "description": "Suspected gas leak near kitchen stove",
    "address": "Flat 302, Sunrise Apartments, Koramangala, Bengaluru - 560095"
}
```

2. New Gas Connection
```json
{
    "request_type": "new_connection",
    "description": "Application for new gas connection",
    "address": "12, Green Valley, Pune - 411001"
}
```

#### 2. View Personal Service Requests
- **Endpoint**: `GET /api/v1/requests/`
- **Behavior**: Shows only requests created by the customer

### Support Representative Endpoints

#### 1. View All Service Requests
- **Endpoint**: `GET /api/v1/requests/`
- **Permissions**: Support Representatives Only
- **Behavior**: Shows all service requests across all customers

#### 2. Update Service Request Status
- **Endpoint**: `PATCH /api/v1/requests/<request_id>/`
- **Permissions**: Support Representatives Only

```json
{
    "status": "in_progress",
    "notes": "Technician assigned for inspection"
}
```

#### 3. Create Request Update
- **Endpoint**: `POST /api/v1/request-updates/`
- **Permissions**: Support Representatives Only

```json
{
    "service_request": 1,
    "status": "resolved",
    "notes": "Gas leak fixed. No further action required."
}
```




## 🛡️ User Profile Management

### Customer Profile Update
- **Endpoint**: `PUT /api/v1/profile/`
```json
{
    "email": "new.anshu@gmail.com",
    "phone_number": "+918765432109",
    "address": "New Apartment, Hyderabad - 500001"
}
```

### Support Representative Profile Update
- **Endpoint**: `PUT /api/v1/profile/`
```json
{
    "email": "abhishek.newmail@gasutility.com",
    "phone_number": "+919988776655"
}
```


## 🚀 Quick Setup
1. Clone repository
2. Create virtual environment
3. Install dependencies: `pip install -r requirements.txt`
4. Run migrations: `python manage.py migrate`
5. Start server: `python manage.py runserver`

## 📝 Additional Notes
- Secure, encrypted communication
- Role-based access control
- Comprehensive input validation
