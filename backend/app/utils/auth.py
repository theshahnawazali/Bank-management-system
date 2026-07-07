# pyright: reportMissingImports=false

import streamlit as st
import extra_streamlit_components as stx
from data.db import cursor, conn

cookie_manager = stx.CookieManager()

def load_user():
    current_user = cookie_manager.get("username")
    chat_id = cookie_manager.get("chat_id")

    return [current_user,chat_id]

def login_user(chat_id,username):

    cookie_manager.set(
        "username",
        username,
        key="token_key",
        expires_at=None
    )

    cookie_manager.set(
        "chat_id",
        chat_id,
        key="chat_id_key",
        expires_at=None
    )


def logout_user():

    cookie_manager.delete(
        "username",
        key="delete_username"
        )
    
    cookie_manager.delete(
        "chat_id",
        key="delete_chat_id"
        )
    
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

def get_user_id(username):
    cursor.execute(f"""
    SELECT user_id FROM users WHERE username = '{username}'
    """)
    user_id = cursor.fetchone()
    return user_id

def session_login(
        user_id       : int,
        session_token : str
):
    cursor.execute("""
        INSERT INTO sessions (user_id,session_token) VALUES (%s, %s)
    """,(
        user_id,
        session_token
        ))
    conn.commit()

def get_user_token(chat_id):
    cursor.execute(f"""
        SELECT session_token FROM sessions WHERE user_id = {chat_id}
    """)

    token = cursor.fetchone()
    return token

def get_user_name(user_id):
    cursor.execute(f"""
    SELECT users.full_name FROM users JOIN sessions ON users.user_id = sessions.user_id WHERE sessions.user_id = {user_id};
""")
    name = cursor.fetchone()
    return name[0]

def get_user_username(user_id):
    cursor.execute(f"""
    SELECT users.username FROM users JOIN sessions ON users.user_id = sessions.user_id WHERE sessions.user_id = {user_id};
""")
    username = cursor.fetchone()
    return username[0]


def delete_sessions(user_id):
    cursor.execute(f"""
        DELETE FROM sessions WHERE user_id = {user_id};
    """)
    conn.commit()