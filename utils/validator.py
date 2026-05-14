# =========================================================
# VALIDATION UTILITIES
# Centralized validation logic for banking system
# =========================================================


# ---------------- USER VALIDATORS -----------------
import streamlit as st
def validate_username(username):
    """
    Ensure username is valid.
    """
    if not username:
        return False

    if len(username) < 4:
        return False
        
    return True


def validate_password(password):
    """
    Validate password strength.
    """
    if len(password) < 8:
        return False
    

    return True


def validate_name(name):
    """
    Validate account holder name.
    """
    if not name.strip():
        return False

    return True


# ---------------- ACCOUNT VALIDATORS ----------------

def validate_account_type(acc_type):
    """
    Validate account type.
    """
    valid = ["Saving Account", "Current Account"]

    if acc_type not in valid:
        raise ValueError("Invalid account type")

    return True


def validate_initial_balance(balance):
    """
    Validate initial deposit.
    """
    
    if balance < 0:
        raise ValueError("Initial balance cannot be negative")

    return True


# ---------------- TRANSACTION VALIDATORS ----------------

def validate_amount(amount):
    """
    Ensure transaction amount is valid.
    """
    if amount <= 0:
        raise ValueError("Amount must be greater than zero")

    return True


def validate_sufficient_balance(balance, amount):
    """
    Check if user has enough balance.
    """
    if amount > balance:
        raise ValueError("Insufficient balance")

    return True


# ---------------- GENERIC VALIDATOR ----------------

def validate_user_logged_in(username):
    """
    Ensure user is authenticated.
    """
    if username == "User":
        raise PermissionError("User must login first")

    return True