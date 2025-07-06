# Sheriff API

A FastAPI-based Discord bot service that manages user pledges and recipients using Stripe for payments and onboarding.

---

## 🚀 Features

- Manage recipients for pledges with Stripe Connect Express accounts
- Generate onboarding links for recipients
- Webhook handling for Stripe events
- BDD tests with Behave
- Integration tests with stripe-mock
- Containerized with Docker and docker-compose for local development

---

## ⚙️ Prerequisites

- Docker
- Docker Compose
- Python 3.10+ (if running locally without Docker)

---

## 🔧 Environment Configuration

Set environment variables in production:

- STRIPE_SECRET_KEY
- STRIPE_WEBHOOK_SECRET
- STRIPE_API_BASE (optional for stripe-mock)
- DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD
- REFRESH_URL, RETURN_URL

---

## 🐳 Running Locally with Docker Compose

1. **Build and start services:**

docker-compose up --build

2. The API will be available at http://localhost:8000.

---

## 🧪 Running Tests

### ✅ Unit & Integration Tests

Run all pytest-based tests:

```
make test
```

or manually:

```
pytest -v
```

### ✅ BDD Tests

Ensure the app and stripe-mock are running, then:

```
make bdd
```

or manually:

```
behave tests/features
```

---

## 🔨 Makefile Targets

```
make install     # Install python dependencies  
make test        # Run pytest unit tests  
make bdd         # Run behave BDD tests
```

---

## 🔗 Useful Endpoints

```
| Method | Path                | Description                                     |
|--------|---------------------|-------------------------------------------------|
| GET    | /health             | Health check                                    |
| POST   | /create_recipient   | Create a new recipient and generate onboarding link |
| GET    | /recipients         | List all recipients                             |
| POST   | /webhook            | Stripe webhook handler                         |
```

---

## 📝 Notes

- Uses **stripe-mock** for safe local testing of Stripe API calls.
- Uses **Postgres** as the database, with schemas initialized at app startup.
- Configured for easy extension with new routes and services.

---

## ✨ Contributing

1. Fork the repository.
2. Create a feature branch (`git checkout -b feature/my-feature`).
3. Commit your changes (`git commit -am 'Add new feature'`).
4. Push to the branch (`git push origin feature/my-feature`).
5. Create a Pull Request.

---

## 📄 License

MIT © Your Name or Organization
