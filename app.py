import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Dashboard - Coleta Centro", layout="wide")

st.markdown(
    """
    <style>
        body {
            background-color: #0e1117;
            color: white;
        }
        .stApp {
            background-color: #0e1117;
            color: white;
        }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("🚛 Dashboard - Coleta Centro")

file = "Coleta centro2.xlsx"
df = pd.read_excel(file)

df.columns = df.columns.str.strip()

df = df[df["Mês"].notna()]
df = df[df["Mês"] != "Total"]

df["Coleta AM"] = pd.to_numeric(df["Coleta AM"], errors='coerce')
df["Coleta PM"] = pd.to_numeric(df["Coleta PM"], errors='coerce')
df["Total"] = pd.to_numeric(df["Total"], errors='coerce')

manha = df["Coleta AM"].sum()
tarde = df["Coleta PM"].sum()
total = df["Total"].sum()

col1, col2, col3 = st.columns(3)
col1.metric("🌅 Manhã (kg)", f"{manha:,.0f}")
col2.metric("🌇 Tarde (kg)", f"{tarde:,.0f}")
col3.metric("📊 Total", f"{total:,.0f}")

st.subheader("📦 Coleta Mensal")
fig_bar = px.bar(
    df,
    x="Total",
    y="Mês",
    color_discrete_sequence=["#00ffff"],
    orientation="h",
    labels={"Mês": "Mês", "Total": "Total (kg)"},
    title="Total Coletado por Mês"
)
fig_bar.update_layout(
    plot_bgcolor="#0e1117",
    paper_bgcolor="#0e1117",
    font_color="white"
)
st.plotly_chart(fig_bar, use_container_width=True)

st.subheader("🍕 Proporção Manhã vs Tarde")
pizza_data = pd.DataFrame({
    "Período": ["Manhã", "Tarde"],
    "Quantidade": [manha, tarde]
})
fig_pie = px.pie(
    pizza_data,
    values="Quantidade",
    names="Período",
    color_discrete_sequence=["#00ffff", "#FF6600"],
    title="Proporção de Coleta Manhã vs Tarde"
)
fig_pie.update_layout(
    plot_bgcolor="#0e1117",
    paper_bgcolor="#0e1117",
    font_color="white"
)
st.plotly_chart(fig_pie, use_container_width=True)

st.subheader("📑 Dados Detalhados")
st.dataframe(df)
