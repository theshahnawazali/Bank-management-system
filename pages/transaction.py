import streamlit as st
from templates import header,sidebar
from services.bank_service import Transactions
from utils.verify_login import verify_login_session


st.set_page_config(page_title="📊 Transactions",layout="wide")


# ----------------- Verify Login ----------------------------
user = verify_login_session()

if user == None:
    st.switch_page("app.py")

# --------------------- Headers -----------------------------
sidebar.sidebar()
header.user_header("Transaction",user["name"])

st.markdown("### 📊 All Transactions")


col_transaction, col_date, col_type, col_amount, col_status = st.columns([1,1,1,1,1])

trans = Transactions(user["username"])


with col_transaction:
    st.write("Trasaction ID")
    for i in range(len(trans.data)):
        st.write(trans.data[i][0])

with col_date:
    st.write("Date")
    for i in range(len(trans.data)):
        st.write(trans.data[i][2])

with col_type:
    st.write("Transaction Type")
    for i in range(len(trans.data)):
        st.write(trans.data[i][1])

with col_amount:
    st.write("Amount")
    for i in range(len(trans.data)):
        st.write(trans.data[i][3])

with col_status:
    st.write("Status")
    for i in range(len(trans.data)):
        st.write(trans.data[i][4])

