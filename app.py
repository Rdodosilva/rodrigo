import pandas as pd
import streamlit as st
import plotly.graph_objects as go

# =============================
# 🖥️ Configuração da Página
# =============================
st.set_page_config(
    page_title="Dashboard - Coleta Centro",
    page_icon="🚛",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =============================
# 🎨 Estilo Personalizado
# =============================
st.markdown(
    """
    <style>
    body {
        background-color: #0f0f0f;
        color: #f0f0f0;
    }
    .stApp {
        background-color: #0f0f0f;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# =============================
# 🔗 Leitura dos Dados
# =============================
try:
    df = pd.read_excel("Coleta centro2.xlsx", sheet_name="Planilha1")

    # Limpar espaços dos nomes das colunas
    df.columns = df.columns.str.strip()

    # Verificar as colunas disponíveis
    st.sidebar.subheader("🛠️ Colunas no arquivo:")
    st.sidebar.write(df.columns.tolist())

    # Validar se existe a coluna 'Mês'
    if "Mês" not in df.columns:
        st.error("❌ A coluna 'Mês' não foi encontrada no arquivo Excel. Verifique se está correta.")
        st.stop()

    # Filtrar linhas com mês preenchido
    df = df[df["Mês"].notna()]

    # Criar colunas de peso
    df["Peso AM (kg)"] = df["Coleta AM"] * 20
    df["Peso PM (kg)"] = df["Coleta PM"] * 20
    df["Peso Total (kg)"] = df["Total de Sacos"] * 20

except Exception as e:
    st.error(f"❌ Erro ao ler o arquivo: {e}")
    st.stop()

# =============================
# 🎛️ Sidebar - Filtros
# =============================
st.sidebar.title("🔎 Filtros")
meses = st.sidebar.multiselect(
    "Selecione o(s) mês(es):",
    options=df["Mês"].unique(),
    default=df["Mês"].unique()
)

df_filtrado = df[df["Mês"].isin(meses)]

# =============================
# 🧠 KPIs
# =============================
total_sacos = df_filtrado["Total de Sacos"].sum()
total_am = df_filtrado["Coleta AM"].sum()
total_pm = df_filtrado["Coleta PM"].sum()

peso_total = total_sacos * 20
peso_am = total_am * 20
peso_pm = total_pm * 20

# =============================
# 🔥 Layout KPIs
# =============================
st.title("🚛 Dashboard - Coleta Centro")

col1, col2, col3 = st.columns(3)

col1.metric("🗑️ Total de Sacos", f"{total_sacos}")
col2.metric("⚖️ Peso Total", f"{peso_total} kg")
col3.metric("🌅 AM / 🌇 PM", f"{total_am} AM / {total_pm} PM")

st.markdown("---")

# =============================
# 📊 Gráfico - Coleta de Sacos
# =============================
fig = go.Figure()

fig.add_trace(go.Bar(
    x=df_filtrado["Mês"],
    y=df_filtrado["Coleta AM"],
    name="Manhã (AM)",
    marker_color="rgb(0, 123, 255)"
))

fig.add_trace(go.Bar(
    x=df_filtrado["Mês"],
    y=df_filtrado["Coleta PM"],
    name="Tarde (PM)",
    marker_color="rgb(255, 140, 0)"
))

fig.update_layout(
    barmode="group",
    title="📦 Coleta de Sacos por Mês e Período",
    xaxis_title="Mês",
    yaxis_title="Quantidade de Sacos",
    template="plotly_dark",
    plot_bgcolor="#0f0f0f",
    paper_bgcolor="#0f0f0f",
    legend_title="Período"
)

st.plotly_chart(fig, use_container_width=True)

# =============================
# 📦 Gráfico - Peso Coletado
# =============================
fig_peso = go.Figure()

fig_peso.add_trace(go.Bar(
    x=df_filtrado["Mês"],
    y=df_filtrado["Peso AM (kg)"],
    name="Manhã (AM)",
    marker_color="rgb(0, 123, 255)"
))

fig_peso.add_trace(go.Bar(
    x=df_filtrado["Mês"],
    y=df_filtrado["Peso PM (kg)"],
    name="Tarde (PM)",
    marker_color="rgb(255, 140, 0)"
))

fig_peso.update_layout(
    barmode="group",
    title="⚖️ Peso Coletado por Mês e Período",
    xaxis_title="Mês",
    yaxis_title="Peso (kg)",
    template="plotly_dark",
    plot_bgcolor="#0f0f0f",
    paper_bgcolor="#0f0f0f",
    legend_title="Período"
)

st.plotly_chart(fig_peso, use_container_width=True)
