import streamlit as st

def sidebar():      
    st.markdown("""
        <style>
        html, body, .stApp {
            background-color: #0d1117 !important;
            color: #e6edf3;
        }

        .stApp > header { background: transparent; }

        section.main > div { padding: 2rem 2.5rem; }
            
        /* ── Our Services ── */
        .our-services  {
            font-size: 1.35rem;
            font-weight: 600;
            color: #e6edf3;
            margin-bottom: 1.5rem;
            letter-spacing: 0.01em;
        }
                
        /* ── Streamlit column padding fix ── */
        [data-testid="stHorizontalBlock"] > div { gap: 1.2rem; }
        [data-testid="column"] > div { padding: 0 !important; }
        </style>
        """,unsafe_allow_html=True)

    # st.markdown('<div class="our-services">Our Services</div>',unsafe_allow_html=True)

    with st.sidebar:
        st.markdown("""
        <style>
        .sidebar-menu  {
            font-size: 1.35rem;
            font-weight: 600;
            color: #e6edf3;
            margin-bottom: 1.5rem;
            letter-spacing: 0.01em;
        }
        </style>
                    """,unsafe_allow_html=True)
        
        st.markdown('<div class="sidebar-menu">Our Services</div>',unsafe_allow_html=True)
        if st.button("🏦 Dashboard"):
            st.switch_page("pages/home.py")

        if st.button("💰 Deposit"):
            st.switch_page("pages/deposit.py")

        if st.button("💸 Withdraw"):
            st.switch_page("pages/withdraw.py")
        
        if st.button("🔄 Transfer"):
            st.switch_page("pages/transfer.py")

        if st.button("📊 Transactions"):
            st.switch_page("pages/transaction.py")