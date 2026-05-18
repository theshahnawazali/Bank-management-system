# pyright: reportMissingImports=false

import streamlit as st
import extra_streamlit_components as stx

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