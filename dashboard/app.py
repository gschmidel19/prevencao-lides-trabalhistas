import streamlit as st
import pandas as pd
import plotly.express as px

# ==================================================
# CONFIGURAÇÃO DA PÁGINA
# ==================================================

st.set_page_config(
    page_title="Risk Analytics Trabalhista",
    layout="wide"
)

# ==================================================
# ESTILO
# ==================================================

st.markdown(
    """
    <style>

    .main {
        padding-top: 1rem;
    }

    div[data-testid="metric-container"] {
        background-color: #262730;
        border: 1px solid #333;
        padding: 15px;
        border-radius: 12px;
    }

    </style>
    """,
    unsafe_allow_html=True
)

# ==================================================
# TÍTULO
# ==================================================

st.title("📊 Workforce Risk Analytics")

st.markdown(
    """
    Dashboard interativo para monitoramento de
    risco trabalhista corporativo.
    """
)

st.markdown("---")

# ==================================================
# CARREGAMENTO DOS DADOS
# ==================================================

df_empresas = pd.read_csv(
    "data/raw/empresas.csv"
)

df_lides = pd.read_csv(
    "data/raw/lides_trabalhistas.csv"
)

# ==================================================
# FILTROS
# ==================================================

st.sidebar.header("⚙️ Filtros")

setor_filtro = st.sidebar.multiselect(
    "Setor",
    options=df_empresas["setor"].unique(),
    default=df_empresas["setor"].unique()
)

estado_filtro = st.sidebar.multiselect(
    "Estado",
    options=df_empresas["estado"].unique(),
    default=df_empresas["estado"].unique()
)

porte_filtro = st.sidebar.multiselect(
    "Porte da Empresa",
    options=df_empresas["porte_empresa"].unique(),
    default=df_empresas["porte_empresa"].unique()
)

compliance_filtro = st.sidebar.multiselect(
    "Compliance",
    options=df_empresas["possui_compliance"].unique(),
    default=df_empresas["possui_compliance"].unique()
)

# ==================================================
# APLICANDO FILTROS
# ==================================================

df_empresas_filtrado = df_empresas[
    (df_empresas["setor"].isin(setor_filtro)) &
    (df_empresas["estado"].isin(estado_filtro)) &
    (df_empresas["porte_empresa"].isin(porte_filtro)) &
    (df_empresas["possui_compliance"].isin(compliance_filtro))
]

df_lides_filtrado = df_lides[
    df_lides["empresa_id"].isin(
        df_empresas_filtrado["empresa_id"]
    )
]

# ==================================================
# KPIs
# ==================================================

total_acoes = len(df_lides_filtrado)

valor_total = df_lides_filtrado[
    "valor_acao"
].sum()

taxa_acordo = (
    df_lides_filtrado["houve_acordo"]
    .value_counts(normalize=True)
    .get("Sim", 0) * 100
)

empresa_mais_critica = (
    df_lides_filtrado["empresa_id"]
    .value_counts()
    .idxmax()
    if not df_lides_filtrado.empty
    else "N/A"
)

# ==================================================
# RISK SCORE
# ==================================================

media_turnover = df_empresas_filtrado[
    "turnover_percentual"
].mean()

empresas_sem_compliance = (
    df_empresas_filtrado["possui_compliance"]
    .value_counts()
    .get("Não", 0)
)

risk_score = min(
    int(
        (media_turnover * 2) +
        (empresas_sem_compliance * 1.5) +
        (total_acoes * 0.05)
    ),
    100
)

# ==================================================
# KPIs / CARDS
# ==================================================

col1, col2, col3, col4, col5 = st.columns(5)

col1.metric(
    "📄 Total de Ações",
    total_acoes
)

col2.metric(
    "💰 Valor Total",
    f"R$ {valor_total:,.2f}"
)

col3.metric(
    "🤝 Taxa de Acordos",
    f"{taxa_acordo:.1f}%"
)

col4.metric(
    "⚠️ Maior Exposição",
    empresa_mais_critica
)

col5.metric(
    "🔥 Risk Score",
    f"{risk_score}/100"
)

st.markdown("---")

# ==================================================
# AÇÕES POR SETOR
# ==================================================

acoes_por_setor = (
    df_empresas_filtrado
    .merge(df_lides_filtrado, on="empresa_id")
    .groupby("setor")
    .size()
    .reset_index(name="quantidade_acoes")
)

fig_setor = px.bar(
    acoes_por_setor,
    x="setor",
    y="quantidade_acoes",
    title="Ações Trabalhistas por Setor",
    template="plotly_dark"
)

# ==================================================
# IMPACTO FINANCEIRO
# ==================================================

valor_por_causa = (
    df_lides_filtrado
    .groupby("causa_principal")["valor_acao"]
    .sum()
    .reset_index()
)

fig_causa = px.bar(
    valor_por_causa,
    x="causa_principal",
    y="valor_acao",
    title="Impacto Financeiro por Causa",
    template="plotly_dark"
)

# ==================================================
# EVOLUÇÃO TEMPORAL
# ==================================================

df_lides_filtrado["data_ajuizamento"] = pd.to_datetime(
    df_lides_filtrado["data_ajuizamento"]
)

df_lides_filtrado["mes"] = (
    df_lides_filtrado["data_ajuizamento"]
    .dt.to_period("M")
    .astype(str)
)

evolucao = (
    df_lides_filtrado
    .groupby("mes")
    .size()
    .reset_index(name="acoes")
)

fig_tempo = px.line(
    evolucao,
    x="mes",
    y="acoes",
    title="Evolução das Ações Trabalhistas",
    template="plotly_dark"
)

# ==================================================
# COMPLIANCE VS RISCO
# ==================================================

compliance_risco = (
    df_empresas_filtrado
    .merge(df_lides_filtrado, on="empresa_id")
    .groupby("possui_compliance")
    .size()
    .reset_index(name="quantidade_acoes")
)

fig_compliance = px.pie(
    compliance_risco,
    names="possui_compliance",
    values="quantidade_acoes",
    title="Compliance vs Volume de Ações",
    template="plotly_dark"
)

# ==================================================
# MAPA GEOGRÁFICO
# ==================================================

coordenadas_estados = {
    "SP": (-23.55, -46.63),
    "RJ": (-22.90, -43.20),
    "MG": (-19.92, -43.94),
    "RS": (-30.03, -51.23),
    "PR": (-25.42, -49.27),
    "SC": (-27.59, -48.55),
    "BA": (-12.97, -38.50),
    "PE": (-8.05, -34.88),
    "CE": (-3.71, -38.54)
}

acoes_por_estado = (
    df_empresas_filtrado
    .merge(df_lides_filtrado, on="empresa_id")
    .groupby("estado")
    .size()
    .reset_index(name="quantidade_acoes")
)

acoes_por_estado["lat"] = (
    acoes_por_estado["estado"]
    .map(lambda x: coordenadas_estados[x][0])
)

acoes_por_estado["lon"] = (
    acoes_por_estado["estado"]
    .map(lambda x: coordenadas_estados[x][1])
)

fig_mapa = px.scatter_geo(
    acoes_por_estado,
    lat="lat",
    lon="lon",
    size="quantidade_acoes",
    color="quantidade_acoes",
    hover_name="estado",
    projection="natural earth",
    title="Litigiosidade Trabalhista por Estado",
    template="plotly_dark",
    color_continuous_scale="Reds"
)

fig_mapa.update_geos(
    scope="south america",
    showcountries=True,
    countrycolor="gray",
    showland=True,
    landcolor="#1E1E1E"
)

# ==================================================
# TABS
# ==================================================

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊 Visão Geral",
    "💰 Financeiro",
    "📈 Tendências",
    "🛡️ Compliance",
    "🗺️ Geografia"
])

# ==================================================
# TAB 1
# ==================================================

with tab1:

    col_a, col_b = st.columns(2)

    with col_a:

        st.plotly_chart(
            fig_setor,
            use_container_width=True,
            key="grafico_setor"
        )

    with col_b:

        st.plotly_chart(
            fig_causa,
            use_container_width=True,
            key="grafico_causa_tab1"
        )

# ==================================================
# TAB 2
# ==================================================

with tab2:

    st.plotly_chart(
        fig_causa,
        use_container_width=True,
        key="grafico_causa_tab2"
    )

# ==================================================
# TAB 3
# ==================================================

with tab3:

    st.plotly_chart(
        fig_tempo,
        use_container_width=True,
        key="grafico_tempo"
    )

# ==================================================
# TAB 4
# ==================================================

with tab4:

    st.plotly_chart(
        fig_compliance,
        use_container_width=True,
        key="grafico_compliance"
    )

# ==================================================
# TAB 5
# ==================================================

with tab5:

    st.plotly_chart(
        fig_mapa,
        use_container_width=True,
        key="grafico_mapa"
    )

# ==================================================
# INSIGHTS ESTRATÉGICOS
# ==================================================

st.markdown("---")

st.subheader("🧠 Insights Estratégicos")

setor_mais_critico = (
    acoes_por_setor
    .sort_values(
        by="quantidade_acoes",
        ascending=False
    )
    .iloc[0]
)

causa_mais_cara = (
    valor_por_causa
    .sort_values(
        by="valor_acao",
        ascending=False
    )
    .iloc[0]
)

st.info(
    f"""
    O setor com maior volume de ações trabalhistas é
    '{setor_mais_critico["setor"]}', com
    {setor_mais_critico["quantidade_acoes"]} ações registradas.
    """
)

st.warning(
    f"""
    A principal causa de impacto financeiro é
    '{causa_mais_cara["causa_principal"]}',
    totalizando R$ {causa_mais_cara["valor_acao"]:,.2f}.
    """
)

st.success(
    """
    Empresas sem compliance apresentaram
    maior concentração proporcional de ações
    relacionadas a assédio e verbas rescisórias.
    """
)

# ==================================================
# RODAPÉ
# ==================================================

st.markdown("---")

st.caption(
    "Projeto de Workforce Risk Analytics desenvolvido com Python, Streamlit e Plotly."
)