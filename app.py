import streamlit as st
import pandas as pd
import plotly.express as px

# Streamlit page config
st.set_page_config(page_title="📱 PhonePe Pulse Dashboard", layout="wide")
st.title("📱 PhonePe Pulse Data Visualizer")
st.caption("A live data exploration dashboard powered by public PhonePe Pulse data.")

# Load datasets
df_txn = pd.read_csv("state_transaction_data.csv")
df_user = pd.read_csv("state_user_device_data.csv")
df_map = pd.read_csv("district_transaction_data.csv")

# Sidebar filters
with st.sidebar:
    st.header("📌 Filters")
    year = st.selectbox("📅 Select Year", sorted(df_txn["year"].unique()))
    quarter = st.selectbox("📆 Select Quarter", sorted(df_txn["quarter"].unique()))
    view_type = st.selectbox("📊 Select View", ["Top States", "Districts", "Device Brands"])

# Filter data
filtered_txn = df_txn[(df_txn["year"] == year) & (df_txn["quarter"] == quarter)]
filtered_map = df_map[(df_map["year"] == year) & (df_map["quarter"] == quarter)]
filtered_user = df_user[(df_user["year"] == year) & (df_user["quarter"] == quarter)]

# Metric summary
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("🧾 Total Transactions", f"{filtered_txn['count'].sum():,}")
with col2:
    st.metric("💸 Total Amount (₹)", f"{filtered_txn['amount'].sum():,.2f}")
with col3:
    st.metric("📱 Unique Device Brands", filtered_user['brand'].nunique())

st.markdown("---")

# Visualization views
if view_type == "Top States":
    st.subheader(f"🏁 Top 10 States by Transaction Amount ({year} Q{quarter})")
    top_states = filtered_txn.groupby("state")["amount"].sum().sort_values(ascending=True).tail(10).reset_index()
    fig = px.bar(
        top_states,
        x="amount",
        y="state",
        orientation="h",
        color="amount",
        color_continuous_scale="Viridis",
        labels={"amount": "₹ Transaction Amount", "state": "State"},
        title="Transaction Amount by State"
    )
    st.plotly_chart(fig, use_container_width=True)

elif view_type == "Districts":
    st.subheader(f"🏙️ Top 10 Districts by Transaction Amount ({year} Q{quarter})")
    top_districts = filtered_map.groupby("district")["amount"].sum().sort_values(ascending=True).tail(10).reset_index()
    fig = px.bar(
        top_districts,
        x="amount",
        y="district",
        orientation="h",
        color="amount",
        color_continuous_scale="Cividis",
        labels={"amount": "₹ Transaction Amount", "district": "District"},
        title="Transaction Amount by District"
    )
    st.plotly_chart(fig, use_container_width=True)

elif view_type == "Device Brands":
    st.subheader(f"📱 Top 10 Device Brands Used ({year} Q{quarter})")
    brand_totals = filtered_user.groupby("brand")["count"].sum().sort_values(ascending=False).head(10).reset_index()
    fig = px.pie(
        brand_totals,
        names="brand",
        values="count",
        hole=0.4,
        title="Top Device Brands (User Count)",
        color_discrete_sequence=px.colors.sequential.Plasma_r
    )
    st.plotly_chart(fig, use_container_width=True)

# Footer
st.markdown("---")
st.markdown(
    "<div style='text-align: center; padding-top: 10px;'>"
    "<small>Made by <strong>Mrityunjay Acharya</strong></small>"
    "</div>",
    unsafe_allow_html=True
)
