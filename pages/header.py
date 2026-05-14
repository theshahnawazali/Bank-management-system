import streamlit as st

def render_header(user_name: str = "Test User"):
    initials = "".join([n[0].upper() for n in user_name.split()[:2]])
    
    st.markdown("""
    <style>
    .header-container {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 0.75rem 1.5rem;
        background: #1e1e2e;
        border-bottom: 1px solid #2e2e3e;
        border-radius: 10px;
        margin-bottom: 1.5rem;
    }
    .company-name {
        display: flex;
        align-items: center;
        gap: 10px;
        font-size: 20px;
        font-weight: 600;
        color: #ffffff;
    }
    .company-logo {
        width: 34px;
        height: 34px;
        background: #1a73e8;
        border-radius: 8px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 16px;
        color: white;
    }
    .right-section {
        display: flex;
        align-items: center;
        gap: 12px;
    }
    .user-badge {
        display: flex;
        align-items: center;
        gap: 8px;
        background: #2e2e3e;
        padding: 5px 14px;
        border-radius: 20px;
        font-size: 14px;
        color: #e0e0e0;
    }
    .avatar {
        width: 26px;
        height: 26px;
        background: #1a73e8;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 11px;
        font-weight: 600;
        color: white;
    }
    .logout-btn {
        background: #1a73e8;
        color: white;
        border: none;
        padding: 6px 16px;
        border-radius: 8px;
        font-size: 14px;
        font-weight: 500;
        cursor: pointer;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="header-container">
        <div class="company-name">
            <div class="company-logo">⚡</div>
            MyCompany
        </div>
        <div class="right-section">
            <div class="user-badge">
                <div class="avatar">{initials}</div>
                {user_name}
            </div>
            <button class="logout-btn">🚪 Logout</button>
        </div>
    </div>
    """, unsafe_allow_html=True)

