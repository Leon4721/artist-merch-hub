# Artist Merch Hub

a Django e-commerce platform for artists to sell music and merchandise directly to their fan base, allow thier fans to build up their own communities.  based of discord and reddit for the Undergound culture. 

**Live Site:** [https://artist-merch-hub.onrender.com/store/](https://artist-merch-hub.onrender.com/store/)

## Purpose

Enable independent artists to sell digital music and merchandise directly to fans with secure Stripe payments and premium content access.

## Features

- User authentication (register/login/logout)
- Product catalog (digital music & merchandise)
- Stripe payment integration
- Premium content access system
- Product reviews and ratings
- Real-time search filtering
- Responsive Bootstrap design

## Data Schema

### Models

**Product**
- title, description, price, product_type, is_premium, created_at

**Review**
- product (FK), user (FK), rating (1-5), comment, timestamps
- Unique constraint: one review per user per product

**Order**
- user (FK), stripe_session_id (unique), amount, currency, status, created_at

**UserProfile**
- user (OneToOne), has_paid, created_at

### Relationships
- User ↔ UserProfile (One-to-One)
- User → Reviews (One-to-Many)
- User → Orders (One-to-Many)
- Product → Reviews (One-to-Many)

## CRUD Operations

- **Create**: Register users, add reviews, process payments
- **Read**: Browse products, view details, search catalog
- **Update**: Edit reviews, update profiles
- **Delete**: Remove reviews, cancel orders

## Technologies

- **Backend**: Django 6.0.1, Python 3.13
- **Database**: SQLite (dev), PostgreSQL (production)
- **Payment**: Stripe API
- **Frontend**: Bootstrap 5, JavaScript
- **Deployment**: Render.com, Gunicorn, WhiteNoise

## Installation
```bash
git clone https://github.com/Leon4721/artist-merch-hub.git
cd artist-merch-hub
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Create `.env` file:
```
SECRET_KEY=your-secret-key
DEBUG=True
STRIPE_PUBLIC_KEY=pk_test_...
STRIPE_SECRET_KEY=sk_test_...
```

## Testing
```bash
python manage.py test
```

Tests cover:
- Model creation and validation
- View responses and authentication
- CRUD operations
- Business logic

## Deployment

Deployed on Render.com with:
- PostgreSQL database
- Environment variables for secrets
- DEBUG=False in production
- Static files via WhiteNoise

## Security

- Secrets in environment variables
- Database excluded from Git
- CSRF protection enabled
- Password validation enforced
- Stripe test mode for development

## Author

Leon Freeman - Code Institute Project 4