import streamlit as st
import pandas as pd

# ==========================================
# CONFIGURAÇÃO DA PÁGINA
# ==========================================

st.set_page_config(
    page_title="MERCADINHO Portal Da Vila",
    page_icon="🛍️",
    layout="wide"
)

# REINTEGRAÇÃO DO MENU LATERAL ORIGINAL
st.sidebar.markdown("# 🏪 Menu Mercadinho")
st.sidebar.write("Ir para:")
st.sidebar.radio("Navegação", ["Dashboard Inicial", "Gestão de Fiados", "Tabelas de Preço"], index=0, label_visibility="collapsed")

# Injeção de CSS para recriar o cabeçalho e os botões roxos com o visual idêntico
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
    
    /* CONTAINER DOS BOTÕES COM ALINHAMENTO ORIGINAL */
    .button-container {
        display: flex;
        gap: 15px;
        margin-bottom: 30px;
        width: 100%;
    }
    
    /* ESTILO DOS BOTÕES ROXOS GRANDES E PREENCHIDOS */
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
# CARREGAMENTO LEVE E EM TEMPO REAL (SEM CACHE)
# ==========================================

ID_PLANILHA = "1u_bK8xpagg6AzDG9Slij9kyAWaa71roChrhCYYqL7ow"
URL_CSV = f"https://google.com{ID_PLANILHA}/gviz/tq?tqx=out:csv&sheet=Clientes"

def carregar_dados_dashboard():
    try:
        # Puxa as linhas diretamente do link público via pandas (evita RefreshError)
        df = pd.read_csv(URL_CSV)
        if df.empty or "Nome" not in df.columns:
            return pd.DataFrame(columns=["Nome", "Limite", "Divida"])
            
        # Converte as colunas financeiras de texto para números reais matemáticos
        df["Divida"] = pd.to_numeric(df["Divida"], errors="coerce").fillna(0.0)
        df["Limite"] = pd.to_numeric(df["Limite"], errors="coerce").fillna(0.0)
        return df[["Nome", "Limite", "Divida"]].dropna(subset=["Nome"])
    except:
        return pd.DataFrame(columns=["Nome", "Limite", "Divida"])

# Baixa os números fresquinhos do Google Drive toda vez que a tela atualiza
df_clientes = carregar_dados_dashboard()
# ==========================================
# CONTEÚDO VISUAL DO DASHBOARD
# ==========================================

# Cabeçalho Principal (Idêntico ao seu print original)
st.markdown("""
    <div class="main-header">
        <span>🛍️ MERCADINHO Portal Da Vila</span>
        <span class="status-bd">🟢 online</span>
    </div>
""", unsafe_allow_html=True)

# Bloco de Botões Roxos com o Alinhamento e Tamanho Perfeitos
st.markdown("""
    <div class="button-container">
        <a href="/Gestao_de_Fiados" target="_self" class="purple-button">👥 PESSOAS</a>
        <a href="/Tabelas_de_Preco" target="_self" class="purple-button">📦 PRODUTOS</a>
        <a href="#" target="_self" class="purple-button">📋 CONTAS A RECEBER</a>
    </div>
""", unsafe_allow_html=True)
    
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
    # Mantido informativo até criarmos a aba de produtos
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
