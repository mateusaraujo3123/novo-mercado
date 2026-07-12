import streamlit as st
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials


# ==========================================
# CONFIGURAÇÃO DA PÁGINA
# ==========================================

st.set_page_config(
    page_title="Gestão de Fiados - Portal da Vila",
    page_icon="🏪",
    layout="wide"
)


# ==========================================
# MENU LATERAL
# ==========================================

st.sidebar.title("🏪 Portal da Vila")

pagina = st.sidebar.radio(
    "Menu",
    [
        "Dashboard",
        "Gestão de Fiados"
    ]
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

    credenciais = Credentials.from_service_account_info(
        st.secrets["gcp_service_account"],
        scopes=SCOPES
    )

    cliente = gspread.authorize(
        credenciais
    )

    return cliente.open_by_key(
        ID_PLANILHA
    )


planilha = conectar_planilha()

aba_clientes = planilha.worksheet("Clientes")



# ==========================================
# CARREGAR CLIENTES
# ==========================================

@st.cache_data(ttl=10)
def carregar_clientes():

    dados = aba_clientes.get_all_records()


    if not dados:

        return pd.DataFrame(
            columns=[
                "Nome",
                "Limite",
                "Divida"
            ]
        )


    df = pd.DataFrame(dados)


    for coluna in [
        "Nome",
        "Limite",
        "Divida"
    ]:

        if coluna not in df.columns:
            df[coluna] = 0


    df["Limite"] = pd.to_numeric(
        df["Limite"],
        errors="coerce"
    ).fillna(0)


    df["Divida"] = pd.to_numeric(
        df["Divida"],
        errors="coerce"
    ).fillna(0)


    return df[
        [
            "Nome",
            "Limite",
            "Divida"
        ]
    ]



# ==========================================
# SALVAR
# ==========================================

def salvar_clientes(df):

    dados = [
        df.columns.tolist()
    ]

    dados += df.values.tolist()


    aba_clientes.clear()

    aba_clientes.update(
        dados
    )


    carregar_clientes.clear()
