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
# GOOGLE SHEETS (LEITURA DIRETA)
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

def buscar_dados_frescos():
    try:
        planilha = conectar_planilha()
        aba_clientes = planilha.worksheet("Clientes")
        dados = aba_clientes.get_all_records()
        
        if not dados:
            return pd.DataFrame(columns=["Nome", "Limite", "Divida"])
            
        df = pd.DataFrame(dados)
        
        for col in ["Nome", "Limite", "Divida"]:
            if col not in df.columns:
                df[col] = 0.0
                
        df["Divida"] = pd.to_numeric(df["Divida"], errors="coerce").fillna(0.0)
        df["Limite"] = pd.to_numeric(df["Limite"], errors="coerce").fillna(0.0)
        return df
    except:
        return pd.DataFrame(columns=["Nome", "Limite", "Divida"])

df_clientes = buscar_dados_frescos()
# ==========================================
# CONTEÚDO VISUAL DO DASHBOARD
# ==========================================

# Cabeçalho Principal (Idêntico ao seu print)
st.markdown("""
    <div class="main-header">
        <span>🛍️ MERCADINHO Portal Da Vila</span>
        <span class="status-bd">🟢 online</span>
    </div>
""", unsafe_allow_html=True)

# Botões de Atalho Superiores com Navegação Segura e Nativa
col_btn1, col_btn2, col_btn3 = st.columns(3)

with col_btn1:
    # Ao clicar, usa a função nativa do Streamlit para ir para o arquivo da pasta pages
    if st.button("👥 PESSOAS", use_container_width=True):
        st.switch_page("pages/1_Pessoas.py")
        
with col_btn2:
    if st.button("📦 PRODUTOS", use_container_width=True):
        # Altere para o nome exato do seu arquivo de produtos quando criá-lo
        st.switch_page("pages/2_Produtos.py")
        
with col_btn3:
    if st.button("📋 CONTAS A RECEBER", use_container_width=True):
        st.info("Aba Contas a Receber em desenvolvimento.")

st.markdown("<br>", unsafe_allow_html=True)
st.markdown("## Fluxo de Fiados & Devedores")

# Seção Central Automatizada (2 colunas)
col_centro1, col_centro2 = st.columns(2)

with col_centro1:
    st.subheader("Top Maiores Devedores (R$)")
    
    # Filtra apenas os clientes que estão devendo e ordena do maior para o menor
    df_devedores = df_clientes[df_clientes["Divida"] > 0].sort_values(by="Divida", ascending=False)
    
    if df_devedores.empty:
        st.info("Nenhuma dívida ativa registrada na planilha.")
    else:
        # Formata os valores exibidos na tabela central
        df_exibir = df_devedores[["Nome", "Divida"]].copy()
        df_exibir["Divida"] = df_exibir["Divida"].map("R$ %.2f".__mod__)
        st.dataframe(df_exibir, use_container_width=True, hide_index=True)
        
with col_centro2:
    st.subheader("⚠️ Alertas do Estoque")
    st.info("Nenhum produto cadastrado na planilha.")
    
st.markdown("---")

# ==========================================
# CÁLCULO E EXIBIÇÃO DE MÉTRICAS REAIS
# ==========================================

soma_fiados = df_clientes["Divida"].sum()

# Identifica clientes que estouraram o limite configurado
clientes_estourados = len(df_clientes[df_clientes["Divida"] > df_clientes["Limite"]])

col_kpi1, col_kpi2, col_kpi3 = st.columns(3)

with col_kpi1:
    st.metric(
        label="Soma Total de Fiados", 
        value=f"R$ {soma_fiados:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    )
    
with col_kpi2:
    st.metric(
        label="Clientes Acima do Limite", 
        value=str(clientes_estourados)
    )
    
with col_kpi3:
    st.metric(
        label="Caixa Estimado do Dia", 
        value="R$ 1.250,00" # Mantido fixo conforme imagem de referência
    )
