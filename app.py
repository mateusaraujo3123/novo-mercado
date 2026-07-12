import streamlit as st
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials

# ==========================================
# CONFIGURAÇÃO DA PÁGINA
# ==========================================

st.set_page_config(
    page_title="MERCADINHO Portal Da Vila",
    page_icon="🛍️",
    layout="wide"
)

# Injeção de CSS para recriar o cabeçalho e os botões roxos no tamanho original
st.markdown("""
    <style>
    .main-header {
        background-color: #6A1B9A !important;
        color: white !important;
        padding: 15px;
        border-radius: 8px;
        font-size: 24px;
        font-weight: bold;
        margin-bottom: 25px;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    .status-bd {
        background-color: #2E7D32 !important;
        color: white !important;
        padding: 5px 10px;
        border-radius: 20px;
        font-size: 14px;
    }
    .button-container {
        display: flex;
        gap: 15px;
        margin-bottom: 30px;
        width: 100%;
    }
    .purple-button {
        flex: 1;
        background-color: #4A148C !important;
        color: white !important;
        padding: 20px 0px;
        text-align: center;
        text-decoration: none !important;
        font-weight: bold;
        font-size: 15px;
        border-radius: 6px;
        box-shadow: 0px 4px 6px rgba(0,0,0,0.2);
        transition: background-color 0.2s ease;
        display: block;
    }
    .purple-button:link, .purple-button:visited, .purple-button:hover, .purple-button:active {
        text-decoration: none !important;
        color: white !important;
    }
    .purple-button:hover {
        background-color: #6A1B9A !important;
    }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# GOOGLE SHEETS (CONEXÃO REAL)
# ==========================================

ID_PLANILHA = "1u_bK8xpagg6AzDG9Slij9kyAWaa71roChrhCYYqL7ow"
SCOPES = [
    "https://googleapis.com",
    "https://googleapis.com"
]

@st.cache_resource
def conectar_planilha():
    creds = Credentials.from_service_account_info(
        st.secrets["gcp_service_account"],
        scopes=SCOPES
    )
    cliente = gspread.authorize(creds)
    return cliente.open_by_key(ID_PLANILHA)

try:
    planilha = conectar_planilha()
    aba_clientes = planilha.worksheet("Clientes")
    dados = aba_clientes.get_all_records()
    df_clientes = pd.DataFrame(dados) if dados else pd.DataFrame(columns=["Nome", "Limite", "Divida"])
except:
    df_clientes = pd.DataFrame(columns=["Nome", "Limite", "Divida"])

# Tratamento e conversão correta dos dados financeiros vindos da planilha
df_clientes["Divida"] = pd.to_numeric(df_clientes["Divida"], errors="coerce").fillna(0.0)
df_clientes["Limite"] = pd.to_numeric(df_clientes["Limite"], errors="coerce").fillna(0.0)
