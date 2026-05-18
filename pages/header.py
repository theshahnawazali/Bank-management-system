import streamlit as st
from utils.auth import logout_user

def render_header(current_user):
    st.markdown("""
    <style>
    /* Sirf last column ka button chhota — yahi logout hai header mein */
    section[data-testid="stSidebar"] ~ div div[data-testid="stColumns"] 
    > div:last-child div.stButton > button {
        width: auto !important;
        height: auto !important;
        min-height: 0 !important;
        padding: 0.4rem 1rem !important;
        font-size: 0.85rem !important;
    }
    </style>
    """, unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns([3, 2, 2, 1])

    with col1:
        st.markdown("## BankCore")

    with col2:
        pass

    with col3:
        if current_user is None:
            if st.button("Signup", key="Signup_button"):
                st.switch_page("pages/signup.py")

    with col4:
        if current_user is None:
            if st.button("Login", key="Login_button"):
                st.switch_page("pages/login.py")
        else:
            if st.button("Logout", key="Logout_button"):
                logout_user()