# SaaS Application

This document provides a summary of a SaaS application built with FastAPI, focusing on its advanced security and authentication features. This project demonstrates how to implement the functionalities of a SaaS in a simple and abstract way.

## Project Structure

The project is organized into several modules, each responsible for a specific feature:

- `main.py`: The main application file, including the FastAPI app instance and router configurations.
- `security.py`: Handles core security features like OAuth2, JWT, and password hashing.
- `models.py`: Defines data models, including the `User` model.
- `operations.py`: Contains business logic for user operations.
- `github_login.py` & `third_party_login.py`: Implements third-party authentication with GitHub.
- `mfa.py`: Implements Multi-Factor Authentication.
- `api_key.py`: Handles API key-based authentication.
- `user_session.py`: Manages user sessions using cookies.
- `rbac.py`: Implements Role-Based Access Control.
- `premium_access.py`: Manages access to premium features.

## Features

### 1. User Registration

- **File:** `main.py`, `operations.py`, `models.py`
- **Endpoint:** `POST /register/user`
- **Description:** New users can register by providing a username, email, and password. The application hashes the password before storing it in the database.

### 2. OAuth2 and JWT Authentication

- **File:** `security.py`
- **Endpoint:** `POST /token` and `GET /users/me`
- **Description:** The application implements OAuth2 with JWT tokens for authentication. Users can request a token by providing their credentials. The application then verifies the credentials and issues a JWT token.

### 3. Role-Based Access Control (RBAC)

- **File:** `rbac.py`
- **Endpoints:** `GET "/welcome/all-users`, `GET /welcome/premium-user`
- **Description:** The application implements RBAC to restrict access to certain endpoints based on user roles. It defines different roles (e.g., `basic`, `premium`) and protects endpoints with dependencies that check the user's role.

### 4. Third-Party Authentication with GitHub

- **File:** `github_login.py`, `third_party_login.py`
- **Endpoints:** `GET /auth/url`, `GET /github/auth/token`
- **Description:** Users can authenticate using their GitHub account. The application provides a URL to redirect the user to GitHub for authorization and then receives a callback with an access token.

### 5. Multi-Factor Authentication (MFA)

- **File:** `mfa.py`
- **Endpoints:** `POST /user/enable-mfa`, `POST /verify-totp`
- **Description:** The application supports MFA using TOTP (Time-based One-Time Password). Users can enable MFA by scanning a QR code with an authenticator app. When logging in, they must provide a TOTP to complete the authentication.

### 6. API Key Authentication

- **File:** `api_key.py`
- **Endpoint:** `GET /secure-data`
- **Description:** The application provides a way to authenticate requests using an API key. Users can obtain an API key and use it in the `X-API-Key` header to access protected endpoints.

### 7. User Session and Cookies

- **File:** `user_session.py`
- **Endpoints:** `POST /login`, `POST /logout`
- **Description:** The application manages user sessions using cookies. After a user logs in, a session token is stored in a cookie. This token is used to authenticate subsequent requests. The application also provides a logout endpoint to clear the session.

### 8. Premium Access

- **File:** `premium_access.py`
- **Endpoint:** `POST /register/premium-user`
- **Description:** The application has a concept of premium access. Certain endpoints are protected and can only be accessed by users with a premium subscription. This is checked via a dependency that verifies the user's subscription status.



Note: To run the project you need an .env file with the following environment variables:

```bash
GITHUB_CLIENT_ID=<YOUR_GENERATED_GITHUB_CLIENT_ID>
GITHUB_CLIENT_SECRET=<YOUR_GENERATED_GITHUB_CLIENT_SECRET>
```

How do I get that data? You need to follow the steps in the video [Sign in with GitHub OAuth in 5 minutes - YouTube](https://youtu.be/Bx1JqfPROXA?si=bBdNgQ_96LbpzRGQ)  starting at 3:43. Obviously, it's registered using the data from the app in this repository. This is a tutorial that can be used as a reference.
