import streamlit as st

def user_overview(data):
    """Renders the main user overview page with account info and services."""

    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;600&display=swap');

    * { font-family: 'Space Grotesk', sans-serif; }

    html, body, .stApp {
        background-color: #0d1117 !important;
        color: #e6edf3;
    }

    .stApp > header { background: transparent; }

    section.main > div { padding: 2rem 2.5rem; }

    /* ── Page Title ── */
    .page-title {
        font-size: 1.35rem;
        font-weight: 600;
        color: #e6edf3;
        margin-bottom: 1.5rem;
        letter-spacing: 0.01em;
    }

    /* ── Card base ── */
    .card {
        background: #161b22;
        border: 1px solid #21262d;
        border-radius: 14px;
        padding: 1.5rem;
        height: 250px;
        box-sizing: border-box;
    }

    /* ── BankCore credit-card widget ── */
    .bank-card {
        background: linear-gradient(135deg, #1c2333 0%, #253048 100%);
        border: 1px solid #30363d;
        border-radius: 16px;
        padding: 1.4rem 1.6rem 1.2rem;
        position: relative;
        overflow: hidden;
        height: 250px;
        box-sizing: border-box;
    }
    .bank-card::before {
        content: '';
        position: absolute;
        top: -40px; right: -40px;
        width: 160px; height: 160px;
        background: radial-gradient(circle, rgba(88,166,255,0.12) 0%, transparent 70%);
        border-radius: 50%;
    }
    .bank-card-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 1.2rem;
    }
    .bank-card-logo {
        font-size: 1.05rem;
        font-weight: 700;
        color: #e6edf3;
        letter-spacing: 0.04em;
    }
    .chip-icon {
        width: 32px; height: 24px;
        background: linear-gradient(135deg, #f0c040, #c8952a);
        border-radius: 5px;
    }
    .card-badge {
        font-size: 0.68rem;
        color: #8b949e;
        background: #21262d;
        border: 1px solid #30363d;
        padding: 2px 8px;
        border-radius: 20px;
    }
    .card-number {
        font-family: 'JetBrains Mono', monospace;
        font-size: 1.02rem;
        color: #c9d1d9;
        letter-spacing: 0.12em;
        margin-bottom: 2rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    .copy-icon { color: #8b949e; font-size: 0.8rem; cursor: pointer; }
    .card-footer { display: flex; justify-content: space-between; }
    .card-footer-label { font-size: 0.68rem; color: #8b949e; text-transform: uppercase; letter-spacing: 0.08em; margin-bottom: 2px; }
    .card-footer-value { font-size: 0.9rem; font-weight: 500; color: #e6edf3; }

    /* ── Detail rows ── */
    .detail-row {
        display: flex;
        align-items: center;
        padding: 0.65rem 0;
        border-bottom: 1px solid #21262d;
        gap: 1rem;
    }
    .detail-row:last-child { border-bottom: none; }
    .detail-icon { font-size: 1rem; color: #8b949e; width: 22px; text-align: center; }
    .detail-label { color: #8b949e; font-size: 0.85rem; flex: 1; }
    .detail-value { font-size: 0.85rem; color: #e6edf3; font-weight: 500; text-align: right; }
    .badge-active {
        background: rgba(35,134,54,0.2);
        color: #3fb950;
        border: 1px solid rgba(63,185,80,0.3);
        padding: 2px 12px;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 600;
    }

    /* ── Balance card ── */
    .balance-label { font-size: 0.75rem; color: #8b949e; margin-bottom: 1px; }
    .balance-amount {
        font-size: 1.7rem;
        font-weight: 700;
        color: #58a6ff;
        font-family: 'JetBrains Mono', monospace;
        letter-spacing: -0.02em;
        margin-bottom: 0.5rem;
    }
    .ledger-label { font-size: 0.78rem; color: #8b949e; margin-bottom: 2px; }
    .ledger-amount { font-size: 1rem; font-weight: 600; color: #e6edf3; font-family: 'JetBrains Mono', monospace; }
    .divider { border: none; border-top: 1px solid #21262d; }

    /* ── CTA Button ── */
    .cta-btn {
        display: block;
        width: 100%;
        background: linear-gradient(135deg, #6e40c9, #58a6ff);
        color: #fff;
        border: none;
        border-radius: 10px;
        padding: 0.7rem 1rem;
        font-size: 0.88rem;
        font-weight: 600;
        text-align: center;
        cursor: pointer;
        letter-spacing: 0.02em;
        margin-top: 1.2rem;
    }


    /* ── Streamlit column padding fix ── */
    [data-testid="stHorizontalBlock"] > div { gap: 1.2rem; }
    [data-testid="column"] > div { padding: 0 !important; }
    </style>
    """, unsafe_allow_html=True)

    # ── Title ──
    st.markdown('<div class="page-title">Account Overview</div>', unsafe_allow_html=True)

    col_card, col_details, col_balance = st.columns([1.15, 1.5, 1])

    # ══ LEFT: BankCore Card ══
    with col_card:
        st.markdown(f"""
        <div class="bank-card">
            <div class="bank-card-header">
                <div style="display:flex;align-items:center;gap:0.6rem;">
                    <div class="chip-icon"></div>
                    <span class="bank-card-logo">BankCore</span>
                </div>
                <span class="card-badge">Primary Account</span>
            </div>
            <div style="font-size:0.7rem;color:#8b949e;margin-bottom:4px;letter-spacing:0.06em;">ACCOUNT NUMBER</div>
            <div class="card-number">
                {data["Account Number"]}
                <span class="copy-icon">⎘</span>
            </div>
            <div class="card-footer">
                <div>
                    <div class="card-footer-label">Account Holder</div>
                    <div class="card-footer-value">{data["name"]}</div>
                </div>
                <div style="text-align:right;">
                    <div class="card-footer-label">Account Type</div>
                    <div class="card-footer-value">{data["Account Type"]}</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # ══ MIDDLE: Account Details ══
    with col_details:
        st.markdown(f"""
        <div class="card">
            <div class="detail-row">
                <span class="detail-icon">👤</span>
                <span class="detail-label">Account Status</span>
                <span class="badge-active">Active</span>
            </div>
            <div class="detail-row">
                <span class="detail-icon">🏦</span>
                <span class="detail-label">Account Type</span>
                <span class="detail-value">{data["Account Type"]}</span>
            </div>
            <div class="detail-row">
                <span class="detail-icon">📅</span>
                <span class="detail-label">Opened On</span>
                <span class="detail-value">{data["Open On"]}</span>
            </div>
            <div class="detail-row">
                <span class="detail-icon">💱</span>
                <span class="detail-label">Currency</span>
                <span class="detail-value">INR</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # ══ RIGHT: Balance Summary ══
    with col_balance:
        st.markdown(f"""
        <div class="card">
            <div style="font-size:0.95rem;font-weight:600;color:#e6edf3;margin-bottom:1rem;">Balance Summary</div>
            <div class="balance-label">Available Balance</div>
            <div class="balance-amount">INR {data["Balance"]}</div>
            <hr class="divider">
            <button class="cta-btn">📄 View Statements</button>
        </div>
        """, unsafe_allow_html=True) 
