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

# Injeção de CSS para recriar os botões e remover de vez o sublinhado
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
    
    /* CONTAINER DOS BOTÕES WITH SIZING CORRETO */
    .button-container {
        display: flex;
        gap: 15px;
        margin-bottom: 30px;
        width: 100%;
    }
    
    /* ESTILO IDENTICO DOS BOTOES ROXOS ORIGINAIS (SEM SUBLINHADO) */
    .purple-button {
        flex: 1;
        background-color: #4A148C !important;
        color: white !important;
        padding: 20px 0px;
        text-align: center;
        text-decoration: none !important; /* Remove a linha de baixo padrão */
        font-weight: bold;
        font-size: 15px;
        border-radius: 6px;
        box-shadow: 0px 4px 6px rgba(0,0,0,0.2);
        transition: background-color 0.2s ease;
        display: block;
    }
    
    /* Força a remoção do sublinhado em todos os estados do botão */
    .purple-button:link, .purple-button:visited, .purple-button:hover, .purple-button:active {
        text-decoration: none !important;
        color: white !important;
    }
    
    .purple-button:hover {
        background-color: #6A1B9A !important;
    }
    </style>
""", unsafe_allow_html=True)
# Cabeçalho Principal (idêntico à imagem)
st.markdown("""
    <div class="main-header">
        <span>🛍️ MERCADINHO Portal Da Vila</span>
        <span class="status-bd">🟢 online</span>
    </div>
""", unsafe_allow_html=True)

# Bloco de Botões corrigido e sem linhas sob o texto
st.markdown("""
    <div class="button-container">
        <a href="/Gestao_de_Fiados" target="_self" class="purple-button">👥 PESSOAS</a>
        <a href="/Tabelas_de_Preco" target="_self" class="purple-button">📦 PRODUTOS</a>
        <a href="#" target="_self" class="purple-button">📋 CONTAS A RECEBER</a>
    </div>
""", unsafe_allow_html=True)
    
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
