from faker import Faker
import pandas as pd
import random

fake = Faker("pt_BR")

# Listas base
estados = ["SP", "RJ", "MG", "RS", "PR", "SC", "BA", "PE"]

setores = [
    "Indústria",
    "Construção",
    "TI",
    "Logística",
    "Comércio",
    "Serviços"
]

portes = ["Pequeno", "Médio", "Grande"]

# Lista onde as empresas serão armazenadas
empresas = []

# Geração de empresas
for i in range(100):

    setor = random.choice(setores)
    porte = random.choice(portes)
    estado = random.choice(estados)

    # Quantidade de funcionários por porte
    if porte == "Grande":
        funcionarios = random.randint(500, 5000)

    elif porte == "Médio":
        funcionarios = random.randint(100, 500)

    else:
        funcionarios = random.randint(10, 100)

    # Salário médio por setor
    if setor == "TI":
        salario_medio = random.randint(5000, 15000)

    elif setor == "Construção":
        salario_medio = random.randint(2200, 5000)

    else:
        salario_medio = random.randint(2500, 8000)

    # Compliance
    possui_compliance = random.choices(
        ["Sim", "Não"],
        weights=[70, 30]
    )[0]

    # Treinamento antiassédio
    possui_treinamento_assedio = random.choices(
        ["Sim", "Não"],
        weights=[75, 25]
    )[0]

    # Indicadores empresariais
    turnover = round(random.uniform(1, 25), 2)

    horas_extras = round(random.uniform(0, 30), 2)

    absenteismo = round(random.uniform(0, 12), 2)

    satisfacao = round(random.uniform(4, 10), 1)

    # Dicionário da empresa
    empresa = {
        "empresa_id": i + 1,
        "empresa_nome": fake.company(),
        "estado": estado,
        "setor": setor,
        "porte_empresa": porte,
        "quantidade_funcionarios": funcionarios,
        "turnover_percentual": turnover,
        "media_horas_extras": horas_extras,
        "indice_absenteismo": absenteismo,
        "possui_compliance": possui_compliance,
        "possui_treinamento_assedio": possui_treinamento_assedio,
        "indice_satisfacao": satisfacao,
        "salario_medio": salario_medio
    }

    empresas.append(empresa)

# Criando DataFrame
df_empresas = pd.DataFrame(empresas)

# Salvando CSV
df_empresas.to_csv("data/raw/empresas.csv", index=False)

print("Arquivo empresas.csv gerado com sucesso!")

# =========================
# GERAÇÃO DE LIDES
# =========================

causas = [
    "Horas Extras",
    "Assédio Moral",
    "Assédio Sexual",
    "FGTS",
    "Verbas Rescisórias",
    "Vínculo Empregatício",
    "Equiparação Salarial",
    "Acidente de Trabalho"
]

tipos_contratacao = ["CLT", "PJ", "Terceirizado", "Estágio"]

resultados = [
    "Procedente",
    "Improcedente",
    "Parcialmente procedente",
    "Arquivada (acordo)"
]

lides = []

# Gerando 1000 ações trabalhistas
for i in range(1000):

    empresa = df_empresas.sample(1).iloc[0]

    setor = empresa["setor"]
    compliance = empresa["possui_compliance"]
    turnover = empresa["turnover_percentual"]

    # Probabilidades por setor
    if setor == "Construção":
        causa = random.choices(
            causas,
            weights=[10, 5, 2, 10, 15, 5, 3, 50]
        )[0]

    elif setor == "TI":
        causa = random.choices(
            causas,
            weights=[40, 20, 5, 5, 10, 5, 10, 5]
        )[0]

    else:
        causa = random.choice(causas)

    # Empresas sem compliance possuem mais assédio
    if compliance == "Não":
        causa = random.choices(
            ["Assédio Moral", "Assédio Sexual", causa],
            weights=[35, 15, 50]
        )[0]

    # Valor da ação
    valor_acao = round(random.uniform(5000, 80000), 2)

    # Probabilidade de acordo
    houve_acordo = random.choices(
        ["Sim", "Não"],
        weights=[65, 35]
    )[0]

    # Resultado final
    resultado = random.choice(resultados)

    lide = {
        "id_acao": i + 1,
        "empresa_id": empresa["empresa_id"],
        "data_ajuizamento": fake.date_between(
            start_date="-3y",
            end_date="today"
        ),
        "tipo_contratacao": random.choice(tipos_contratacao),
        "causa_principal": causa,
        "valor_acao": valor_acao,
        "houve_acordo": houve_acordo,
        "resultado_final": resultado,
        "tempo_empresa_colaborador": round(random.uniform(0.5, 15), 1),
        "afastamento_previo": random.choice(["Sim", "Não"])
    }

    lides.append(lide)

# Criando dataframe das lides
df_lides = pd.DataFrame(lides)

# Salvando CSV
df_lides.to_csv(
    "data/raw/lides_trabalhistas.csv",
    index=False
)

print("Arquivo lides_trabalhistas.csv gerado com sucesso!")