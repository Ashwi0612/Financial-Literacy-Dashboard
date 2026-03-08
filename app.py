# ============================================================
# Financial Literacy Dashboard for College Students
# Built with Python + Streamlit + Pandas + Matplotlib
# ============================================================

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

# ── Page config ──────────────────────────────────────────────
st.set_page_config(
    page_title="FinLit Dashboard",
    page_icon="💰",
    layout="wide"
)

# ── Custom CSS ────────────────────────────────────────────────
st.markdown("""
<style>
    .main { background-color: #0a0a0f; }
    .block-container { padding-top: 2rem; }
    h1, h2, h3 { color: #6ee7b7; }
    .stMetric { background: #12121a; padding: 1rem; border-radius: 10px; }
    .tip-box {
        background: #12121a;
        border-left: 4px solid #6ee7b7;
        padding: 12px 16px;
        border-radius: 6px;
        margin: 8px 0;
        color: #e2e8f0;
        font-size: 14px;
    }
</style>
""", unsafe_allow_html=True)

# ── Sample Data ───────────────────────────────────────────────
# This is sample data representing a typical college student's monthly finances
# In a real version, users can upload their own data

@st.cache_data
def load_sample_data():
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
              "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

    data = {
        "Month": months,
        "Income":    [5000, 5000, 5500, 5000, 5000, 6000,
                      5000, 5000, 5500, 5000, 5000, 7000],
        "Food":      [1200, 1100, 1300, 1250, 1150, 1400,
                      1100, 1200, 1300, 1250, 1350, 1500],
        "Transport": [600,  550,  700,  600,  580,  650,
                      500,  600,  700,  620,  600,  700],
        "Education": [800,  800,  800,  800,  800,  800,
                      800,  800,  800,  800,  800,  800],
        "Entertainment": [400, 350, 500, 450, 380, 600,
                          300, 400, 450, 420, 500, 800],
        "Savings":   [1000, 1200, 1000, 900, 1090, 1550,
                      1300, 1000, 950, 910, 750, 1200],
        "Other":     [1000, 1000, 1200, 1000, 1000, 1000,
                      1000, 1000, 1300, 1000, 1000, 2000],
    }
    df = pd.DataFrame(data)
    df["Total_Spent"] = df[["Food","Transport","Education","Entertainment","Other"]].sum(axis=1)
    df["Net_Savings"] = df["Income"] - df["Total_Spent"]
    return df

df = load_sample_data()

EXPENSE_COLS = ["Food", "Transport", "Education", "Entertainment", "Other"]
COLORS = ["#6ee7b7", "#818cf8", "#f472b6", "#fbbf24", "#38bdf8"]

# ── Sidebar ───────────────────────────────────────────────────
st.sidebar.title("💰 FinLit Dashboard")
st.sidebar.markdown("**Financial Literacy for College Students**")
st.sidebar.markdown("---")

selected_month = st.sidebar.selectbox(
    "📅 View Month Details",
    options=df["Month"].tolist(),
    index=len(df) - 1
)

monthly_budget = st.sidebar.number_input(
    "🎯 Set Your Monthly Budget (₹)",
    min_value=1000,
    max_value=50000,
    value=4500,
    step=500
)

st.sidebar.markdown("---")
st.sidebar.markdown("### 📌 Quick Tips")
tips = [
    "Save at least 20% of your income",
    "Track every expense, even small ones",
    "Avoid impulse spending on entertainment",
    "Build an emergency fund first",
]
for tip in tips:
    st.sidebar.markdown(f'<div class="tip-box">💡 {tip}</div>', unsafe_allow_html=True)

# ── Header ────────────────────────────────────────────────────
st.title("💰 Financial Literacy Dashboard")
st.markdown("*Helping college students understand and manage their money better*")
st.markdown("---")

# ── KPI Metrics Row ───────────────────────────────────────────
month_data = df[df["Month"] == selected_month].iloc[0]

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        label="💵 Monthly Income",
        value=f"₹{month_data['Income']:,}",
    )
with col2:
    st.metric(
        label="💸 Total Spent",
        value=f"₹{month_data['Total_Spent']:,}",
        delta=f"-₹{month_data['Total_Spent']:,}"
    )
with col3:
    savings_pct = round((month_data['Net_Savings'] / month_data['Income']) * 100, 1)
    st.metric(
        label="🏦 Net Savings",
        value=f"₹{month_data['Net_Savings']:,}",
        delta=f"{savings_pct}% of income"
    )
with col4:
    budget_status = month_data['Total_Spent'] - monthly_budget
    st.metric(
        label="🎯 vs Your Budget",
        value=f"₹{monthly_budget:,}",
        delta=f"{'Over' if budget_status > 0 else 'Under'} by ₹{abs(budget_status):,}",
        delta_color="inverse"
    )

st.markdown("---")

# ── Charts Row 1 ─────────────────────────────────────────────
col_left, col_right = st.columns(2)

with col_left:
    st.subheader(f"📊 Spending Breakdown — {selected_month}")

    fig1, ax1 = plt.subplots(figsize=(6, 5))
    fig1.patch.set_facecolor("#12121a")
    ax1.set_facecolor("#12121a")

    values = [month_data[col] for col in EXPENSE_COLS]
    wedges, texts, autotexts = ax1.pie(
        values,
        labels=EXPENSE_COLS,
        colors=COLORS,
        autopct="%1.1f%%",
        startangle=90,
        wedgeprops=dict(linewidth=2, edgecolor="#0a0a0f")
    )
    for text in texts:
        text.set_color("#e2e8f0")
        text.set_fontsize(11)
    for autotext in autotexts:
        autotext.set_color("#0a0a0f")
        autotext.set_fontweight("bold")

    ax1.set_title(f"Where did ₹{month_data['Total_Spent']:,} go?",
                  color="#6ee7b7", fontsize=13, pad=15)
    st.pyplot(fig1)
    plt.close()

with col_right:
    st.subheader("📈 Income vs Spending (Full Year)")

    fig2, ax2 = plt.subplots(figsize=(6, 5))
    fig2.patch.set_facecolor("#12121a")
    ax2.set_facecolor("#12121a")

    x = np.arange(len(df["Month"]))
    width = 0.35

    bars1 = ax2.bar(x - width/2, df["Income"], width, label="Income",
                    color="#6ee7b7", alpha=0.9)
    bars2 = ax2.bar(x + width/2, df["Total_Spent"], width, label="Spent",
                    color="#f472b6", alpha=0.9)

    ax2.set_xticks(x)
    ax2.set_xticklabels(df["Month"], color="#e2e8f0", fontsize=9)
    ax2.tick_params(colors="#e2e8f0")
    ax2.spines[:].set_color("#1e1e2e")
    ax2.yaxis.label.set_color("#e2e8f0")
    ax2.set_ylabel("Amount (₹)", color="#e2e8f0")
    ax2.set_title("Monthly Income vs Expenses", color="#6ee7b7", fontsize=13)
    ax2.legend(facecolor="#12121a", labelcolor="#e2e8f0")
    ax2.set_facecolor("#12121a")

    st.pyplot(fig2)
    plt.close()

# ── Charts Row 2 ─────────────────────────────────────────────
col_left2, col_right2 = st.columns(2)

with col_left2:
    st.subheader("💹 Savings Trend (Full Year)")

    fig3, ax3 = plt.subplots(figsize=(6, 4))
    fig3.patch.set_facecolor("#12121a")
    ax3.set_facecolor("#12121a")

    ax3.fill_between(df["Month"], df["Net_Savings"],
                     alpha=0.3, color="#6ee7b7")
    ax3.plot(df["Month"], df["Net_Savings"],
             color="#6ee7b7", linewidth=2.5, marker="o", markersize=5)
    ax3.axhline(y=df["Net_Savings"].mean(), color="#fbbf24",
                linestyle="--", linewidth=1.5, label=f"Avg: ₹{df['Net_Savings'].mean():.0f}")

    ax3.tick_params(colors="#e2e8f0")
    ax3.spines[:].set_color("#1e1e2e")
    ax3.set_ylabel("Savings (₹)", color="#e2e8f0")
    ax3.set_title("Monthly Savings Over the Year", color="#6ee7b7", fontsize=13)
    ax3.legend(facecolor="#12121a", labelcolor="#e2e8f0")

    st.pyplot(fig3)
    plt.close()

with col_right2:
    st.subheader("🏷️ Category Spending Trend")

    fig4, ax4 = plt.subplots(figsize=(6, 4))
    fig4.patch.set_facecolor("#12121a")
    ax4.set_facecolor("#12121a")

    for col, color in zip(EXPENSE_COLS, COLORS):
        ax4.plot(df["Month"], df[col], label=col,
                 color=color, linewidth=2, marker="o", markersize=3)

    ax4.tick_params(colors="#e2e8f0")
    ax4.spines[:].set_color("#1e1e2e")
    ax4.set_ylabel("Amount (₹)", color="#e2e8f0")
    ax4.set_title("Spending per Category — Full Year", color="#6ee7b7", fontsize=13)
    ax4.legend(facecolor="#12121a", labelcolor="#e2e8f0", fontsize=8)

    st.pyplot(fig4)
    plt.close()

# ── Summary Table ─────────────────────────────────────────────
st.markdown("---")
st.subheader("📋 Full Year Summary")

summary = df[["Month", "Income", "Total_Spent", "Net_Savings"]].copy()
summary["Savings %"] = ((summary["Net_Savings"] / summary["Income"]) * 100).round(1).astype(str) + "%"
summary["Income"] = summary["Income"].apply(lambda x: f"₹{x:,}")
summary["Total_Spent"] = summary["Total_Spent"].apply(lambda x: f"₹{x:,}")
summary["Net_Savings"] = summary["Net_Savings"].apply(lambda x: f"₹{x:,}")

st.dataframe(summary, use_container_width=True, hide_index=True)

# ── Financial Health Score ────────────────────────────────────
st.markdown("---")
st.subheader("🏅 Financial Health Score")

avg_savings_pct = (df["Net_Savings"] / df["Income"]).mean() * 100
months_positive = (df["Net_Savings"] > 0).sum()

score = 0
score += min(40, avg_savings_pct * 2)       # up to 40 pts for savings rate
score += (months_positive / 12) * 40        # up to 40 pts for consistency
score += 20 if avg_savings_pct >= 20 else 10 # bonus for hitting 20% rule

score = round(min(100, score))

if score >= 80:
    grade, color, msg = "A", "#6ee7b7", "Excellent! You're managing money very well."
elif score >= 60:
    grade, color, msg = "B", "#fbbf24", "Good! A few tweaks can get you to excellent."
elif score >= 40:
    grade, color, msg = "C", "#f472b6", "Average. Focus on reducing unnecessary expenses."
else:
    grade, color, msg = "D", "#ef4444", "Needs improvement. Start tracking every expense."

col_score, col_msg = st.columns([1, 3])
with col_score:
    st.markdown(f"""
    <div style="background:#12121a; border-radius:16px; padding:24px; text-align:center;
                border: 2px solid {color}44;">
        <div style="font-size:52px; font-weight:900; color:{color};">{grade}</div>
        <div style="font-size:28px; color:{color}; font-weight:700;">{score}/100</div>
        <div style="color:#64748b; font-size:12px; margin-top:4px;">Financial Health Score</div>
    </div>
    """, unsafe_allow_html=True)

with col_msg:
    st.markdown(f"""
    <div style="background:#12121a; border-radius:16px; padding:24px; height:100%;
                border: 1px solid #1e1e2e;">
        <div style="color:{color}; font-size:16px; font-weight:700; margin-bottom:12px;">{msg}</div>
        <div style="color:#e2e8f0; font-size:13px; line-height:1.8;">
            📊 Average savings rate: <b style="color:{color};">{avg_savings_pct:.1f}%</b><br>
            📅 Positive savings months: <b style="color:{color};">{months_positive}/12</b><br>
            🎯 20% savings rule: <b style="color:{color};">{'✅ Met' if avg_savings_pct >= 20 else '❌ Not yet — aim higher'}</b><br>
            💡 Top expense category: <b style="color:{color};">{df[EXPENSE_COLS].mean().idxmax()}</b>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ── Footer ────────────────────────────────────────────────────
st.markdown("---")
st.markdown(
    "<div style='text-align:center; color:#64748b; font-size:12px;'>"
    "Built with ❤️ using Python & Streamlit · "
    "Data is sample data for demonstration purposes"
    "</div>",
    unsafe_allow_html=True
)
