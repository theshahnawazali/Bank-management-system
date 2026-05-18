import streamlit as st
from pages.header import render_header
from utils.auth import load_user
from services.bank_service import Transactions


st.set_page_config(page_title="📊 Transactions",layout="wide")
current_user = load_user()
render_header(current_user)

st.markdown("### 📊 All Transactions")

st.write("Will implemented soon")