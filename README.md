# Secure Messaging Application

A Flask-based secure messaging application that demonstrates hybrid encryption, secure authentication, protected key storage, and encrypted message handling.

## Features

- User registration and login
- bcrypt password hashing
- AES-256-GCM message encryption
- RSA-2048 key generation
- RSA-OAEP with SHA-256 for AES key protection
- Encrypted private-key storage
- CSRF protection
- Protected authenticated routes
- SQLite database storage
- Bandit static security testing

## Technology Stack

- Python
- Flask
- Flask-Login
- Flask-SQLAlchemy
- Flask-Bcrypt
- Flask-WTF
- Cryptography
- SQLite
- HTML / CSS

## Encryption Design

Each message is encrypted with a newly generated AES-256 key using AES-GCM.

The AES key is then encrypted with the recipient's RSA public key using RSA-OAEP with SHA-256.

The database stores:

- encrypted message ciphertext
- encrypted AES key
- nonce
- sender and recipient identifiers

The recipient's protected private key is used by the application to recover the AES key and decrypt the message.

## Security Controls

The application includes:

- password hashing with bcrypt
- CSRF protection
- authenticated route protection
- encrypted private-key storage
- AES-GCM integrity verification
- randomized message encryption
- generic invalid-login responses
- static code analysis with Bandit

## Project Structure

```text
secure-messaging-flask/
|-- app/
|   |-- models/
|   |-- routes/
|   |-- static/
|   `-- templates/
|-- crypto/
|   |-- aes_utils.py
|   `-- rsa_utils.py
|-- config.py
|-- run.py
|-- requirements.txt
|-- .env.example
`-- Secure_Messaging_Report.pdf
```

## Installation

Clone the repository:

```bash
git clone https://github.com/obadah-loul/secure-messaging-flask.git
cd secure-messaging-flask
```

Create a virtual environment:

```bash
python -m venv venv
```

Activate it on Windows:

```powershell
venv\Scripts\Activate.ps1
```

Activate it on Linux:

```bash
source venv/bin/activate
```

Install the required packages:

```bash
pip install -r requirements.txt
```

Create a `.env` file based on `.env.example`.

Example:

```env
SECRET_KEY=replace-with-your-secret-key
PRIVATE_KEY_ENCRYPTION_KEY=replace-with-your-fernet-key
```

Generate a Fernet key:

```bash
python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"
```

Run the application:

```bash
python run.py
```

Open the application in a browser:

```text
http://127.0.0.1:5000
```

## Security Testing

The project was tested for:

- AES-256-GCM encryption and decryption
- ciphertext tampering rejection
- encrypted database storage
- bcrypt password hashing
- authenticated route protection
- invalid-login handling
- CSRF protection
- RSA key storage
- ciphertext randomization
- Bandit static analysis

## Report

The full implementation and security testing report is available here:

[Secure Messaging Report](Secure_Messaging_Report.pdf)

## Limitations

This application is a security engineering prototype and is not intended for production use.

The application server has access to the private-key encryption key and performs message decryption. For that reason, this project should not be described as true end-to-end encryption.

## Purpose

This project demonstrates practical secure software development concepts, including authentication, cryptography, access control, secure storage, and application security testing.