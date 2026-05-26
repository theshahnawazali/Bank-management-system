# header.py
import streamlit as st

st.set_page_config(
    page_title="BankCore",
    page_icon="🏦",
    layout="wide"
    )

from pages.header import render_header


if "user" not in st.session_state:
    st.session_state.current_user = None

render_header(st.session_state.current_user)



st.title("🏦 Banking Management System")

st.write("""
A fully modular web-based Banking Management System developed using Python and Object-Oriented Programming (OOP) concepts.

This project simulates a real banking backend system including authentication, account management, transaction processing, session handling, and persistent database storage.
""")

st.divider()

# Features Section
st.header("📌 Features")

st.subheader("🔐 Authentication & Session Management")
st.write("""
- User Signup & Login System
- Secure Password Hashing
- Random Session ID Generation
- Session Validation using Cookies & Database
- Unique Username Validation
- Multi-user Authentication Support
- Login Session Verification
""")

st.subheader("🏦 Banking Functionalities")
st.write("""
- Savings & Current Account Support
- Automatic Account Number Generation
- Deposit & Withdraw Operations
- Balance Inquiry
- Fund Transfer Between Users
- Unique Transaction ID Generation
- Transaction History Management
""")

st.subheader("💾 Database & Storage")
st.write("""
- MySQL Database Integration
- Persistent Data Storage
- Session Storage Management
- Transaction Records Handling
""")

st.subheader("🎨 Frontend & UI")
st.write("""
- Streamlit-based Web Application
- Interactive Banking Dashboard
- Organized Multi-page Navigation
- Responsive UI Structure
""")

st.divider()

# Project Structure
st.header("🗂 Project Structure")

st.code("""
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
""", language="bash")

st.divider()

# Run Section
st.header("▶️ How to Run")

st.code("""
# Create Virtual Environment
python -m venv venv

# Activate Environment

# Windows
venv\\Scripts\\activate

# Mac/Linux
source venv/bin/activate

# Install Dependencies
pip install -r requirements.txt

# Run Application
streamlit run main.py
""", language="bash")

st.divider()

# Architecture
st.header("📊 Architecture")

st.write("""
User Interface (Streamlit)
        ↓
Main Application
        ↓
Service Layer
        ↓
Model Layer
        ↓
MySQL Database
""")

st.divider()

# Concepts
st.header("🧠 Tech & Concepts")

col1, col2 = st.columns(2)

with col1:
    st.subheader("OOP Concepts")
    st.write("""
- Encapsulation
- Inheritance
- Polymorphism
- Abstraction
""")

with col2:
    st.subheader("Software Design")
    st.write("""
- Layered Architecture
- Separation of Concerns
- Error Handling
- Modular Programming
""")

st.divider()

# Security Section
st.header("🔒 Security Features")

st.write("""
- Password Hashing
- Session ID Validation
- Cookie-based Authentication
- Unique Transaction IDs
- Secure Database Verification
""")

st.divider()

# Future Enhancements
st.header("🔮 Future Enhancements")

st.write("""
- Migration from Streamlit to Flask-based Professional UI
- Admin Dashboard
- Loan Management System
- EMI Calculation System
- REST API Development
- Email & OTP Verification
""")

st.divider()

st.caption(
    "Built as a learning project to strengthen real-world Python, backend development, and system design skills."
)