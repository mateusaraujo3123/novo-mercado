import streamlit as st
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials

# ==========================================
# CONFIGURAÇÃO DA PÁGINA
# ==========================================

st.set_page_config(
    page_title="Gestão de Fiados - Portal da Vila",
    page_icon="👥",
    layout="wide"
)

# ==========================================
# MENU LATERAL
# ==========================================

st.sidebar.markdown("# 🏪 Menu Mercadinho")

st.sidebar.radio(
    "Navegação",
    [
        "Dashboard Inicial",
        "Gestão de Fiados",
        "Tabelas de Preço"
    ],
    index=1,
    label_visibility="collapsed"
)

# ==========================================
# GOOGLE SHEETS
# ==========================================

ID_PLANILHA = "1u_bK8xpagg6AzDG9Slij9kyAWaa71roChrhCYYqL7ow"

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]


@st.cache_resource
def conectar_planilha():

    creds = Credentials.from_service_account_info(
        st.secrets["gcp_service_account"],
        scopes=SCOPES
    )

    cliente = gspread.authorize(creds)

    planilha = cliente.open_by_key(ID_PLANILHA)

    return planilha


planilha = conectar_planilha()

aba_clientes = planilha.worksheet("Clientes")

# ==========================================
# CARREGAR CLIENTES
# ==========================================

@st.cache_data(ttl=5)
def carregar_clientes():

    dados = aba_clientes.get_all_records()

    if len(dados) == 0:

        return pd.DataFrame(
            columns=[
                "Nome",
                "Limite",
                "Divida"
            ]
        )

    df = pd.DataFrame(dados)

    colunas = ["Nome", "Limite", "Divida"]

    for coluna in colunas:

        if coluna not in df.columns:

            df[coluna] = ""

    return df[colunas]

# ==========================================
# SALVAR PLANILHA
# ==========================================

def salvar_clientes(df):

    dados = [df.columns.tolist()]

    dados.extend(df.values.tolist())

    aba_clientes.clear()

    aba_clientes.update(dados)

    carregar_clientes.clear()

# ==========================================
# SESSION STATE
# ==========================================

if "clientes" not in st.session_state:

    st.session_state.clientes = carregar_clientes()

# ==========================================
# TÍTULO
# ==========================================

st.title("👥 Gestão de Clientes")

st.divider()

# Inclusão de todas as abas requisitadas no menu de navegação
aba_lista, aba_novo, aba_adicionar, aba_abater, aba_excluir = st.tabs(
    [
        "📋 Clientes",
        "➕ Novo Cliente",
        "✍️ Adicionar Compra",
        "💰 Receber Pagamento",
        "❌ Remover Cliente"
    ]
)
