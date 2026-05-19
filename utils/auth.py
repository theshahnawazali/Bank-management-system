# pyright: reportMissingImports=false

import streamlit as st
import extra_streamlit_components as stx
from data.db import cursor, conn
cookie_manager = stx.CookieManager()

def load_user():

    if "current_user" not in st.session_state:
        st.session_state.current_user = cookie_manager.get("username")

    return st.session_state.current_user


def login_user(username):

    st.session_state.current_user = username

    cookie_manager.set(
        "username",
        username,
        expires_at=None
    )


def logout_user():

    cookie_manager.delete("username")

    st.session_state.current_user = None


def create_account_handle(
        user_id   : str,
        account_number : int,
        account_type : str,
        balance   : int,
        status    : str
):
    cursor.execute("""
        INSERT INTO accounts (user_id,account_number, account_type, balance, status) VALUES (%s, %s, %s, %s, %s)
    """,(user_id,account_number,account_type,balance,status))

    conn.commit()

def signup_handle(
        full_name : str,
        username  : str,
        password  : str
):
    cursor.execute("""
        INSERT INTO users (full_name,username,password) VALUES (%s, %s, %s)
        """,(full_name,username,password))
    
    conn.commit()

    return cursor.lastrowid

def login_handle(username):
    username = username.lower().strip()
    cursor.execute(f"""
        SELECT password FROM users WHERE username = '{username}';
    """)
    data = cursor.fetchone()
    return data

