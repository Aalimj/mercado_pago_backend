# Changelog

All notable changes to this project will be documented in this file.

## [Unreleased]
- Added user registration endpoint
- Implemented custom user model with email authentication
- Validated email and password during registration
- Passwords are securely hashed

## [0.1.0] - 2025-12-XX
- Initial project setup
- Admin panel configured
- Custom User model created
### 2025-12-15
- Add .env
- fixed the database in postgerSQL
- connected to DBeaver
- added docker-compose.yml
- added Dockerfile


### 2025-12-15
- fixed the wallet and registration 
- fixed the user and registration 

### 2025-12-17
- adding User login endpoint (`POST /api/v1/users/login/`)

## [Unreleased]

### Added
- User login endpoint with JWT authentication (access + refresh tokens)
- Protected profile endpoint (`/api/v1/users/profile/`)
- JWT-based authentication using `djangorestframework-simplejwt`
### Changed
- Switched REST framework authentication from SessionAuthentication to JWTAuthentication
- Improved authentication flow for mobile and frontend clients

### Security
- Secured protected endpoints to require a valid JWT access token

### [] - 2025-12-18
- added account number creating automatic

- 2025-12-18 - Added deposit to the wallet 