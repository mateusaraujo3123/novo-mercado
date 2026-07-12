import streamlit as st
import pandas as pd

# ==========================================
# CONFIGURAÇÃO DA PÁGINA
# ==========================================
st.set_page_config(
    page_title="Tabela de Preços - Portal da Vila",
    page_icon="📦",
    layout="wide"
)

# ==========================================
# MENU LATERAL ADAPTADO
# ==========================================
st.sidebar.markdown("# 🏪 Menu Mercadinho")
st.sidebar.radio(
    "Navegação",
    ["Dashboard Inicial", "Gestão de Fiados", "Tabelas de Preço", "Histórico de Logs"],
    index=2,
    label_visibility="collapsed"
)

# ==========================================
# LEITURA DIRETA, LEVE E BLINDADA CONTRA QUEDAS
# ==========================================
ID_PLANILHA = "1u_bK8xpagg6AzDG9Slij9kyAWaa71roChrhCYYqL7ow"
URL_CSV = f"https://google.com{ID_PLANILHA}/gviz/tq?tqx=out:csv&sheet=Produtos"

def carregar_produtos():
    try:
        # Puxa os dados como link público, sem travar chaves do Google ou memória cache
        df = pd.read_csv(URL_CSV)
        if df.empty or "Produto" not in df.columns:
            return pd.DataFrame(columns=["Produto", "Preco", "Estoque"])
        
        # Garante o formato decimal correto para preços e inteiro para o estoque
        df["Preco"] = pd.to_numeric(df["Preco"], errors="coerce").fillna(0.0)
        df["Estoque"] = pd.to_numeric(df["Estoque"], errors="coerce").fillna(0).astype(int)
        return df[["Produto", "Preco", "Estoque"]].dropna(subset=["Produto"])
    except:
        return pd.DataFrame(columns=["Produto", "Preco", "Estoque"])

df_produtos = carregar_produtos()

# ==========================================
# TÍTULO E DESIGN
# ==========================================
st.title("📦 Tabela de Preços & Estoque")
st.markdown("Consulte os valores das mercadorias e a quantidade disponível no inventário em tempo real.")
st.divider()

aba_consulta = st.tabs(["📋 Catálogo de Produtos"])[0]
# ==========================================
# EXIBIÇÃO DO CATÁLOGO COM FILTRO DE BUSCA
# ==========================================
if df_produtos.empty:
    st.info("Nenhum produto cadastrado na aba 'Produtos' da sua planilha.")
else:
    # Barra de busca rápida por digitação (Deixa o sistema inteligente)
    busca = st.text_input("🔍 Buscar Produto por Nome", placeholder="Digite o nome da mercadoria...").strip().lower()
    
    # Aplica o filtro de busca caso o usuário digite algo
    if busca:
        df_exibir = df_produtos[df_produtos["Produto"].astype(str).str.lower().str.contains(busca)]
    else:
        df_exibir = df_produtos.copy()
        
    if df_exibir.empty:
        st.warning("Nenhuma mercadoria encontrada com esse nome.")
    else:
        # Exibe a planilha de forma limpa e bonita com formatação de moeda
        st.dataframe(
            df_exibir,
            use_container_width=True,
            hide_index=True,
            column_config={
                "Produto": st.column_config.TextColumn("Descrição da Mercadoria"),
                "Preco": st.column_config.NumberColumn("Preço de Venda", format="R$ %.2f"),
                "Estoque": st.column_config.NumberColumn("Qtd. Estoque", format="%d u")
            }
        )

# ==========================================
# RODAPÉ COM INDICADORES GERAIS
# ==========================================
st.divider()

total_itens = len(df_produtos)
total_unidades = pd.to_numeric(df_produtos["Estoque"], errors="coerce").fillna(0).sum()
valor_total_estoque = (
    pd.to_numeric(df_produtos["Preco"], errors="coerce").fillna(0.0) * 
    pd.to_numeric(df_produtos["Estoque"], errors="coerce").fillna(0.0)
).sum()

c1, c2, c3 = st.columns(3)

with c1:
    st.metric("Variedade de Itens", f"{total_itens} produtos")

with c2:
    st.metric("Total em Estoque", f"{int(total_unidades)} und")

with c3:
    st.metric(
        "Valor do Estoque",
        f"R$ {valor_total_estoque:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    )

st.divider()
st.caption("Portal da Vila • Catálogo de Preços")
