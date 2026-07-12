import streamlit as st
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials

st.set_page_config(page_title="Histórico de Logs - Portal da Vila", page_icon="📋", layout="wide")

st.sidebar.markdown("# 🏪 Menu Mercadinho")
st.sidebar.radio("Navegação", ["Dashboard Inicial", "Gestão de Fiados", "Tabelas de Preço", "Histórico de Logs"], index=3, label_visibility="collapsed")

ID_PLANILHA = "1u_bK8xpagg6AzDG9Slij9kyAWaa71roChrhCYYqL7ow"
SCOPES = ["https://googleapis.com", "https://googleapis.com"]

@st.cache_resource
def conectar_planilha():
    creds = Credentials.from_service_account_info(st.secrets["gcp_service_account"], scopes=SCOPES)
    cliente = gspread.authorize(creds)
    return cliente.open_by_key(ID_PLANILHA)

planilha = conectar_planilha()
aba_logs = planilha.worksheet("Logs")

st.title("📋 Histórico de Movimentações")
st.markdown("Veja aqui o registro de todas as compras, pagamentos e cadastros realizados no sistema.")
st.divider()

# Carrega os registros salvos na nuvem
try:
    dados = aba_logs.get_all_records()
    if len(dados) == 0:
        st.info("Nenhuma movimentação registrada no histórico ainda.")
    else:
        df_logs = pd.DataFrame(dados)
        # Inverte a ordem para que o lançamento mais novo apareça no topo da tela
        df_logs = df_logs.iloc[::-1]
        
        # Formata a coluna de valor para ficar bonita na tabela
        df_logs["Valor (R$)"] = pd.to_numeric(df_logs["Valor (R$)"], errors="coerce").fillna(0.0)
        df_logs["Valor (R$)"] = df_logs["Valor (R$)"].map("R$ %.2f".__mod__)
        
        st.dataframe(df_logs, use_container_width=True, hide_index=True)
except:
    st.error("Erro ao carregar a tabela de histórico.")
