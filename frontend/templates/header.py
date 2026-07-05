import streamlit as st
from backend.app.utils.auth import logout_user
def user_header(page,name):
    st.markdown("""
        <style>
        html, body, .stApp {
            background-color: #0d1117 !important;
            color: #e6edf3;
        }

        .stApp > header { background: transparent; }

        section.main > div { padding: 2rem 2.5rem; }
            
        .wlc-msg {
                display : flex;
                flex-direction:column;
        }
        .user-title  {
            font-size: 1.35rem;
            font-weight: 600;
            color: #e6edf3;
            letter-spacing: 0.01em;
        }
        .address {
                font-size:15px;
                color: grey;
        }
                
        /* ── Streamlit column padding fix ── */
        [data-testid="stHorizontalBlock"] > div { gap: 1.2rem; }
        [data-testid="column"] > div { padding: 0 !important; }
        </style>
        """,unsafe_allow_html=True)
    
    col_user, col_logout = st.columns([5,1])

    with col_user:
        st.markdown(f"""
        <div class='wlc-msg'>
            <span class='user-title'>Hello {name} 👋</span>
            <span class='address'>Dashboard > {page}</span>
        </div>
        """, unsafe_allow_html=True)

    with col_logout:
        logout = st.button("Logout", key="User-logout-btn")


    if logout:
        logout_user()