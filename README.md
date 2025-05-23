# 10-Django-Coderr

Project runs at http://127.0.0.1:8000/

This project is a backend API for a marketplace platform similar to Fiverr, where users can create and order professional service offers.

## Overview
* The platform allows users to register as either business accounts or customer accounts.
* Business users can create, update, and manage service offers with detailed options such as pricing, delivery time, and features.
* Customers can browse available offers, place orders on desired services, and leave reviews for the businesses they have worked with.

## Features
* User registration and authentication with token-based access.
* Separate profile types: BusinessProfile and CustomerProfile.
* Businesses can create multiple offers with detailed service packages.
* Customers can order specific offer details.
* Customers can leave ratings and reviews for business services.
* Role-based permissions to secure access and operations (only businesses can create offers, only order owners or staff can update/delete orders, etc.).
* Supports CRUD operations for offers, orders, and reviews.

## Technologies
* Python & Django REST Framework
* Token authentication
* Role-based permission system

## ✅ Requirements

- Python 3.10+
- pip

## 📦 Main Libraries

Django==5.2.1
djangorestframework==3.16.0
django-cors-headers==4.7.0
django-filter==25.1

## 🚀 Setup

```bash
# 1. Clone repository
git clone git@github.com:lindaoest/10-Django-Coderr.git
cd your-project

# 2. (Optional) Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run migrations
python manage.py migrate

# 5. Start server
python manage.py runserver