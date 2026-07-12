import streamlit as st

# Configuração da página em modo amplo
st.set_page_config(
    page_title="MERCADINHO Portal Da Vila",
    page_icon="🛍️",
    layout="wide"
)

# REINTEGRAÇÃO DO MENU LATERAL
st.sidebar.markdown("# 🏪 Menu Mercadinho")
st.sidebar.write("Ir para:")
st.sidebar.radio("Navegação", ["Dashboard Inicial", "Gestão de Fiados", "Tabelas de Preço"], index=0, label_visibility="collapsed")

# Injeção de CSS para o cabeçalho e fixação do tamanho original dos botões
st.markdown("""
    <style>
    /* Cabeçalho principal */
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
    
    /* LIMITAÇÃO DE TAMANHO PARA OS BOTÕES VOLTAREM AO ORIGINAL */
    div[data-testid="stHorizontalBlock"] {
        max-width: 950px; /* Impede que os botões estiquem demais para a direita */
    }
    
    /* Estilização interna do botão roxo */
    div.stButton > button {
        background-color: #4A148C !important;
        color: white !important;
        padding: 18px 0px !important; /* Altura ideal idêntica à imagem */
        border-radius: 6px !important;
        font-weight: bold !important;
        font-size: 15px !important;  
        width: 100% !important;       
        display: block !important;
        border: none !important;
        box-shadow: 0px 4px 6px rgba(0,0,0,0.2);
    }
    div.stButton > button:hover {
        background-color: #6A1B9A !important;
        color: white !important;
        border: none !important;
    }
    </style>
""", unsafe_allow_html=True)

# Cabeçalho Principal
st.markdown("""
    <div class="main-header">
        <span>🛍️ MERCADINHO Portal Da Vila</span>
        <span class="status-bd">🟢 online</span>
    </div>
""", unsafe_allow_html=True)

# Linha de botões com controle de largura máxima ativo
col_btn1, col_btn2, col_btn3 = st.columns(3)
with col_btn1:
    st.button("👥 PESSOAS")
with col_btn2:
    st.button("📦 PRODUTOS")
with col_btn3:
    st.button("📋 CONTAS A RECEBER")
    
st.markdown("<br>", unsafe_allow_html=True)
st.markdown("## Fluxo de Fiados & Devedores")

# Seção Central de Alertas e Maiores Devedores
col_centro1, col_centro2 = st.columns(2)

with col_centro1:
    st.subheader("Top Maiores Devedores (R$)")
    st.info("Nenhuma dívida ativa registrada na planilha.")
    
with col_centro2:
    st.subheader("⚠️ Alertas do Estoque")
    st.info("Nenhum produto cadastrado na planilha.")
    
st.markdown("---")

# Rodapé com Indicadores Numéricos (Métricas KPI)
col_kpi1, col_kpi2, col_kpi3 = st.columns(3)
with col_kpi1:
    st.metric(label="Soma Total de Fiados", value="R$ 0,00")
with col_kpi2:
    st.metric(label="Clientes Acima do Limite", value="0")
with col_kpi3:
    st.metric(label="Caixa Estimado do Dia", value="R$ 1.250,00")
