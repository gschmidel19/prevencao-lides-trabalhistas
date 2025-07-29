
import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title='Análise de Lides Trabalhistas', layout='wide')

@st.cache_data
def carregar_dados():
    return pd.read_csv('lides_trabalhistas_simulado.csv', parse_dates=['data_ajuizamento'])

df = carregar_dados()

st.title('📊 Painel de Lides Trabalhistas')
aba = st.sidebar.radio('Selecione a aba:', ['Visão Geral', 'Recomendações'])

if aba == 'Visão Geral':
    st.subheader('Distribuição por Estado')
    fig_estado = px.histogram(df, x='estado', color='procedente', barmode='group', title='Ações por Estado e Resultado')
    st.plotly_chart(fig_estado, use_container_width=True)

    st.subheader('Distribuição por Cargo')
    fig_cargo = px.histogram(df, x='cargo', color='procedente', barmode='group', title='Ações por Cargo e Resultado')
    st.plotly_chart(fig_cargo, use_container_width=True)

elif aba == 'Recomendações':
    st.subheader('🔍 Recomendações Preventivas')
    cargos_risco = df[df['procedente'] == 'Sim']['cargo'].value_counts().head(5)
    st.write('Cargos com mais ações procedentes:')
    st.table(cargos_risco)

    st.markdown('''
    ### Sugestões:
    - Reforçar treinamentos para os cargos acima.
    - Implementar canais de escuta ativa e compliance.
    - Monitorar turnos e carga horária para evitar passivos.
    - Investir em ações de clima organizacional e feedbacks contínuos.
    ''')

    st.info('Essas recomendações são baseadas em padrões observados no dataset simulado.')

