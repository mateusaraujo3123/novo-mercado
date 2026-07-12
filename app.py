import streamlit as st
import pandas as pd

# Configuração da página para layout amplo (wide)
st.set_page_config(
    page_title="Mercadinho Pro",
    page_icon="🛍️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilização CSS personalizada para imitar as cores da imagem
st.markdown("""
    <style>
    .main-header {
        background-color: #6A1B9A;
        color: white;
        padding: 15px;
        border-radius: 8px;
        font-size: 24px;
        font-weight: bold;
        margin-bottom: 20px;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    .status-bd {
        background-color: #2E7D32;
        color: white;
        padding: 5px 10px;
        border-radius: 20px;
        font-size: 14px;
    }
    .btn-box {
        background-color: #4A148C;
        color: white;
        padding: 20px;
        border-radius: 8px;
        text-align: center;
        font-weight: bold;
        margin-bottom: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# --- MENU LATERAL ---
st.sidebar.markdown("# 🏪 Menu Mercadinho")
st.sidebar.write("Ir para:")
paginas = ["Dashboard Inicial", "Gestão de Fiados", "Tabelas de Preço"]
selecao_pagina = st.sidebar.radio("Navegação", paginas, label_visibility="collapsed")

# --- CONTEÚDO PRINCIPAL ---
if selecao_pagina == "Dashboard Inicial":
    
    # Cabeçalho Principal do Painel
    st.markdown("""
        <div class="main-header">
            <span>🛍️ MERCADINHO PRO</span>
            <span class="status-bd">🟢 BANCO DE DADOS ATIVO</span>
        </div>
    """, unsafe_allow_html=True)
    
    # Botões de Ação Rápida Superiores (3 colunas)
    col_btn1, col_btn2, col_btn3 = st.columns(3)
    with col_btn1:
        st.markdown('<div class="btn-box">👥 PESSOAS</div>', unsafe_allow_html=True)
    with col_btn2:
        st.markdown('<div class="btn-box">📦 PRODUTOS</div>', unsafe_allow_html=True)
    with col_btn3:
        st.markdown('<div class="btn-box">📋 CONTAS A RECEBER</div>', unsafe_allow_html=True)
        
    st.markdown("---")
    st.markdown("## Fluxo de Fiados & Devedores")
    
    # Seção Central: Alertas e Maiores Devedores (2 colunas)
    col_centro1, col_centro2 = st.columns(2)
    
    with col_centro1:
        st.subheader("Top Maiores Devedores (R$)")
        # Simulação de dados vazios como na imagem do usuário
        st.info("Nenhuma dívida ativa registrada na planilha.")
        
    with col_centro2:
        st.subheader("⚠️ Alertas do Estoque")
        st.info("Nenhum produto cadastrado na planilha.")
        
    st.markdown("---")
    
    # Rodapé com Indicadores (Métricas KPI)
    col_kpi1, col_kpi2, col_kpi3 = st.columns(3)
    with col_kpi1:
        st.metric(label="Soma Total de Fiados", value="R$ 0,00")
    with col_kpi2:
        st.metric(label="Clientes Acima do Limite", value="0")
    with col_kpi3:
        st.metric(label="Caixa Estimado do Dia", value="R$ 1.250,00")

elif selecao_pagina == "Gestão de Fiados":
    st.title("👥 Gestão de Fiados")
    st.write("Área para cadastrar clientes e gerenciar limites de crédito.")
    # Aqui você pode adicionar formulários de cadastro futuramente

elif selecao_pagina == "Tabelas de Preço":
    st.title("📋 Tabelas de Preço")
    st.write("Visualização e edição do catálogo de produtos.")
