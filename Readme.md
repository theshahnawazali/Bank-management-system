# 🏦 Banking Management System

A fully modular web-based **Banking Management System** developed using **Python** and **Object-Oriented Programming (OOP)** concepts.

This project simulates the core functionalities of a real banking backend system including authentication, account management, transaction processing, and persistent data storage.

The application is designed using a **layered architecture approach** to ensure scalability, maintainability, and clean code organization.

---

# 📌 Key Features

## 🔐 Authentication & Session Management

* User Signup & Login System
* Secure Password Hashing
* Random Session ID Generation
* Session Validation using Cookies & Database
* Unique Username Validation
* Multi-user Authentication Support
* Login Session Verification

## 🏦 Banking Functionalities

* Savings & Current Account Support
* Automatic Account Number Generation
* Deposit & Withdraw Operations
* Balance Inquiry
* Fund Transfer Between Users
* Unique Transaction ID Generation
* Transaction History Management

## 💾 Database & Storage

* MySQL Database Integration
* Persistent Data Storage
* Session Storage Management
* Transaction Records Handling

## 🎨 Frontend & UI

* Streamlit-based Web Application
* Interactive Banking Dashboard
* User-friendly Banking Interface
* Organized Multi-page Navigation
* Responsive UI Structure

## 🛠 Software Engineering Features

* Modular Project Structure
* Layered Architecture Design
* Separation of Concerns
* Error Handling & Input Validation
* Reusable OOP Components

---

# 🧠 Concepts Used

This project demonstrates practical implementation of:

## Object-Oriented Programming (OOP)

* Encapsulation
* Inheritance
* Polymorphism
* Abstraction

## Software Design Principles

* Layered Architecture
* Modular Programming
* Separation of Concerns
* Reusable Code Design

## Core Python Concepts

* File Handling
* Database Connectivity
* Session Management
* Cookie Handling
* Exception Handling
* Input Validation
* Functions & Modules

---

# 🗂 Project Structure

```bash
bank_project/
│
├── models/               # Account classes & database models
├── services/             # Business logic layer
├── utils/                # Helper functions & validations
├── data/                 # Database & storage configuration
│   └── db.py             # MySQL database connection settings
├── pages/                # Streamlit application pages
├── templates/            # HTML templates for future Flask UI
├── main.py               # Main application entry point
├── requirements.txt      # Project dependencies
└── README.md             # Project documentation
```

---

# ⚙️ System Workflow

```text
User Interface (Streamlit)
        ↓
Main Application
        ↓
Service Layer
        ↓
Model Layer
        ↓
MySQL Database
```

---

# 🚀 How the System Works

1. User signs up or logs into the system
2. Authentication layer validates credentials
3. User creates a bank account
4. System generates a unique account number
5. User performs banking operations
6. Transaction data and sessions are stored securely in MySQL database
7. User can access transaction history anytime

---

# ▶️ Installation & Setup

## Create Virtual Environment

```bash
python -m venv venv
```

## Activate Virtual Environment

### Windows

```bash
venv\Scripts\activate
```

### Mac/Linux

```bash
source venv/bin/activate
```

## Install Dependencies

```bash
pip install -r requirements.txt
```

## Generate Requirements File

```bash
pip freeze > requirements.txt
```

## Run the Application

```bash
streamlit run main.py
```

---

# 📊 Architecture Overview

The project follows a clean layered architecture:

```text
Presentation Layer  →  Service Layer  →  Model Layer  →  Storage Layer
```

## Advantages of This Architecture

* Better scalability
* Easy maintenance
* Cleaner codebase
* Improved readability
* Easier debugging & testing

---

# ⚙️ Database Configuration

Update your database credentials inside:

```bash
data/db.py
```

Modify the following values according to your MySQL setup:

```python
host = "localhost"
user = "your_username"
password = "your_password"
database = "bank_management_system"
```

---

# 🔒 Security Features

* Password hashing for secure authentication
* Random session ID generation
* Session validation using cookies and database matching
* Unique transaction ID generation
* Input validation to prevent invalid operations
* Secure authentication handling
* Error handling for safe transactions

---

# 🎯 Learning Outcomes

Through this project, the following concepts were learned and implemented:

* Designing real-world software systems
* Building scalable Python applications
* Managing users and authentication systems
* Applying OOP concepts practically
* Structuring large projects professionally
* Implementing persistent data storage
* Handling transactions and validations

---

# 🔮 Future Enhancements

Planned improvements for upcoming versions:

* Migration from Streamlit to Flask-based Professional Web UI
* Complete Admin Dashboard
* Loan Management System
* EMI Calculation System
* Credit/Debit Card Features
* REST API Development
* Email & OTP Verification
* User Profile Management
* Notification System
* Docker Deployment
* Unit Testing & Automation
* Advanced Transaction Analytics

---

# 🏁 Conclusion

This Banking Management System is more than a basic Python project — it is a mini backend banking prototype that demonstrates practical software engineering principles using Python.

The project highlights the implementation of clean architecture, modular coding practices, authentication systems, transaction management, and persistent data handling in a real-world inspired application.

---

# 👨‍💻 Tech Stack

* Python
* Object-Oriented Programming (OOP)
* MySQL
* Streamlit
* Session & Cookie Management
* File Handling
* Flask (Planned)

---

⭐ *Built as a learning project to strengthen real-world programming and system design skills.*