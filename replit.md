# WhatsApp Cloud API Webhook Service

## Overview

This project is a Flask-based webhook service designed to integrate with WhatsApp Cloud API. The application serves as a bridge between WhatsApp Business messaging and custom business logic, handling webhook verification and incoming message processing. The service is built to be lightweight and easily deployable, focusing on real-time message handling and API integrations.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Backend Architecture
- **Framework**: Flask web framework chosen for its simplicity and lightweight nature
- **Language**: Python for rapid development and extensive library ecosystem
- **Request Handling**: RESTful webhook endpoint (`/webhook`) that handles both GET (verification) and POST (message processing) requests
- **Environment Configuration**: Uses python-dotenv for environment variable management, enabling secure credential handling across different deployment environments

### Authentication & Security
- **Webhook Verification**: Implements Meta's webhook verification challenge protocol using verify tokens
- **API Authentication**: WhatsApp Cloud API integration using bearer token authentication
- **Session Management**: Flask session management with configurable secret keys
- **Environment Security**: Sensitive credentials (tokens, secrets) stored in environment variables rather than code

### Logging & Monitoring
- **Structured Logging**: Comprehensive logging system with timestamps, log levels, and formatted output
- **Request Tracking**: Detailed logging of webhook verification attempts and message processing
- **Error Handling**: Structured error handling for webhook operations

### Application Flow
- **Verification Flow**: Handles Meta's webhook verification challenge by validating mode, token, and returning challenge
- **Message Processing**: Processes incoming WhatsApp messages through dedicated handler functions
- **Modular Design**: Separation of concerns with dedicated functions for verification and message handling

## External Dependencies

### WhatsApp Cloud API
- **Meta WhatsApp Business Platform**: Primary integration for receiving and sending WhatsApp messages
- **Webhook Protocol**: Implements Meta's webhook specification for real-time message delivery
- **Authentication**: Uses WhatsApp API tokens for secure communication

### Python Libraries
- **Flask**: Core web framework for HTTP request handling
- **python-dotenv**: Environment variable management for configuration
- **Standard Logging**: Built-in Python logging for application monitoring

### Environment Variables
- `VERIFY_TOKEN`: Token used for webhook verification with Meta
- `WHATSAPP_TOKEN`: Authentication token for WhatsApp Cloud API
- `SESSION_SECRET`: Flask session encryption key

### Deployment Requirements
- Python runtime environment
- HTTP server capability for webhook endpoint exposure
- Environment variable configuration support
- Internet connectivity for WhatsApp API communication