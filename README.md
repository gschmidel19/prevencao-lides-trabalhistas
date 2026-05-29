# 📊 Workforce Risk Analytics

Dashboard interativo de análise de risco trabalhista desenvolvido com Python, Streamlit e Plotly, com foco em identificação de padrões de litigiosidade, impacto financeiro e geração de insights estratégicos para prevenção de ações trabalhistas.

---

## 🚀 Objetivo do Projeto

O projeto foi desenvolvido para simular um ambiente corporativo de monitoramento de risco trabalhista, permitindo:

* Identificar setores mais expostos a ações trabalhistas
* Analisar impacto financeiro das principais causas
* Monitorar tendências de litigiosidade ao longo do tempo
* Avaliar relação entre compliance e volume de ações
* Gerar insights estratégicos para prevenção de riscos corporativos

---

## 🧠 Principais Funcionalidades

✅ Dashboard interativo em Streamlit
✅ KPIs executivos em tempo real
✅ Filtros dinâmicos por:

* setor
* estado
* porte da empresa
* compliance

✅ Visualizações analíticas com Plotly
✅ Geração automatizada de dados simulados
✅ Score de risco trabalhista
✅ Insights estratégicos automáticos
✅ Estrutura organizada para evolução futura

---

## 📈 KPIs Monitorados

* Total de ações trabalhistas
* Valor total das ações
* Taxa de acordos
* Empresa com maior exposição
* Risk Score corporativo

---

## 📊 Visualizações Disponíveis

### 📌 Ações Trabalhistas por Setor

Identifica os setores com maior volume de litigiosidade.

### 💰 Impacto Financeiro por Causa

Mostra quais causas geram maior impacto financeiro para as empresas.

### 📈 Evolução Temporal

Acompanha tendências de crescimento ou redução das ações trabalhistas.

### 🛡️ Compliance vs Volume de Ações

Avalia a relação entre práticas de compliance e litigiosidade.

---

## 🛠️ Tecnologias Utilizadas

* Python
* Pandas
* Plotly
* Streamlit
* Faker
* VS Code

---

## 📂 Estrutura do Projeto

```bash
prevencao-lides-trabalhistas/
│
├── .streamlit/
│   └── config.toml
│
├── assets/
│
├── dashboard/
│   └── app.py
│
├── data/
│   └── raw/
│       ├── empresas.csv
│       └── lides_trabalhistas.csv
│
├── notebooks/
│
├── src/
│   └── generate_data.py
│
├── requirements.txt
└── README.md
```

---

## ▶️ Como Executar

### 1. Clone o repositório

```bash
git clone https://github.com/gschmidel19/prevencao-lides-trabalhistas.git
```

### 2. Acesse a pasta do projeto

```bash
cd prevencao-lides-trabalhistas
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

### 4. Gere os dados simulados

```bash
python src/generate_data.py
```

### 5. Execute o dashboard

```bash
python -m streamlit run dashboard/app.py
```

---

## 📸 Preview do Dashboard

> Adicione screenshots do dashboard na pasta `/assets`

Exemplo:

```markdown
![Dashboard](assets/dashboard_overview.png)
```

---

## 🔥 Possíveis Evoluções Futuras

* Machine Learning para previsão de risco trabalhista
* Heatmap geográfico por estado
* Deploy em Streamlit Cloud
* Integração com banco de dados SQL
* Exportação de relatórios em PDF
* Sistema de alertas automáticos

---

## 📌 Motivação

A prevenção de lides trabalhistas pode gerar redução significativa de custos corporativos, além de melhorar compliance, clima organizacional e tomada de decisão baseada em dados.

Este projeto busca unir:

* análise de dados
* business intelligence
* analytics corporativo
* prevenção jurídica
* visualização estratégica

---

## 👨‍💻 Autor

Gabriel Schmidel

* Python
* Data Analytics
* Business Intelligence
* Automação
* Analytics Jurídico

LinkedIn e portfólio em atualização.
