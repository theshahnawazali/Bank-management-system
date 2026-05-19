import streamlit as st
from utils import validator, generator
from services.auth_service import Signup
from utils.hash import hash_password
from models.saving import saving_account 
from models.current import Current_account
from pages.header import render_header
from utils.auth import login_user


render_header(st.session_state.current_user)

st.markdown("### 👤 User Sign Up")

with st.form("sign-up"):
    name = st.text_input("Enter Your Good Name",placeholder="Name")
    username = st.text_input("Enter Unique username",placeholder="Username")
    password = st.text_input('Enter Password',type="password",placeholder="Password")
    re_password = st.text_input("Re Enter Password",placeholder="Password",type="password")
    account_type = st.selectbox(
        "Select Account Type",
        ["Saving Account","Current Account"]
    )
    initial_amount = st.text_input("Enter Initial Amount",placeholder="Enter Amount")
    Button = st.form_submit_button("Signup")


if Button:
    if name == "":
        st.error("Name cannot be empty")

    if password == "" or re_password == "":
        st.error("Password cannot be empty")

    if password != re_password:
        st.error("Password is not same")

    if initial_amount == "":
        st.error("Initial Amount cannot be empty")

    if validator.validate_name(name):
        if validator.validate_username(username):
            username = username.lower().strip()
            unique_username = generator.check_username(username)
            if unique_username:
                if validator.validate_password(password):
                    secured_password = hash_password(password)
                    user_id = Signup(
                        name,
                        username,
                        secured_password
                    )
                    if validator.validate_account_type(account_type):
                        account_number = generator.generate_acc()
                        
                        if validator.validate_initial_balance(int(initial_amount)):
                            if account_type == "Saving Account":
                                # Creating a Saving account
                                saving_account(
                                    user_id.user_id,
                                    name,account_type,
                                    account_number,
                                    initial_amount
                                )
                                
                                # login_user(username)
                                st.success("Account Created")
                                # st.switch_page("pages/home.py")
                            else:
                                Current_account(name, account_type, account_number, initial_amount, username)
                                st.success("Account Created")
                                # st.session_state.current_user = username
                                # st.switch_page("pages/home.py")
                        else:
                            st.error("Amount Should be greater then 0")

                    else:
                        st.write("Musibat")
                else:
                    st.error("Password must be atleast 8 characters long")
            else:
                st.error("Username is already taken. Try another")
        else:
            st.error("Username must be at least 4 characters")