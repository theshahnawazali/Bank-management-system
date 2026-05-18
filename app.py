# header.py
import streamlit as st
from pages.header import render_header


st.set_page_config(page_title="BankCore", page_icon="🏦",layout="wide")

if "user" not in st.session_state:
    st.session_state.current_user = None

render_header(st.session_state.current_user)


st.title("🏦 Banking Management System")
st.write("A console-based banking system built with Python and Object-Oriented Programming.")

st.divider()

st.header("Features")
st.write("""
- User Signup & Login with password hashing
- Savings and Current account types
- Auto-generated unique account numbers
- Deposit, Withdraw, and Transfer money
- Transaction history logs
- JSON-based persistent storage
- Multi-user support
""")

st.header("Project Structure")
st.code("""
bank_project/
├── models/      # Account classes & data models
├── services/    # Business logic layer
├── utils/       # Helper functions
├── data/        # JSON storage files
└── app.py      # Entry point
""")

st.header("How to Run")
st.code("pip install -r requirements.txt\nstreamlit run app.py", language="bash")

st.header("Architecture")
st.write("User Input → Main → Services → Models → Storage")

st.header("Tech & Concepts")
col1, col2 = st.columns(2)
with col1:
    st.write("**OOP Concepts**")
    st.write("- Encapsulation\n- Inheritance\n- Polymorphism")
with col2:
    st.write("**Design**")
    st.write("- Layered Architecture\n- Separation of Concerns\n- Error Handling")

st.divider()
st.caption("Built as a learning project to strengthen real-world Python and system design skills.")