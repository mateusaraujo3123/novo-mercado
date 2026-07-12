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
# COORDENADAS INTERNET DA PLANILHA (SEM CHAVES)
# ==========================================
ID_PLANILHA = "1u_bK8xpagg6AzDG9Slij9kyAWaa71roChrhCYYqL7ow"

# Link público em formato CSV para puxar os dados sem usar tokens do Google
URL_CSV = f"https://google.com{ID_PLANILHA}/gviz/tq?tqx=out:csv&sheet=Produtos"

def carregar_produtos():
    try:
        # Puxa os dados direto da internet pelo pandas comum, ignorando travas de cache
        df = pd.read_csv(URL_CSV)
        if df.empty or "Produto" not in df.columns:
            return pd.DataFrame(columns=["Produto", "Preco"])
        df["Preco"] = pd.to_numeric(df["Preco"], errors="coerce").fillna(0.0)
        return df[["Produto", "Preco"]].dropna(subset=["Produto"])
    except:
        return pd.DataFrame(columns=["Produto", "Preco"])

# Baixa os números do catálogo diretamente da internet a cada F5
df_produtos = carregar_produtos()

# ==========================================
# TÍTULO
# ==========================================
st.title("📦 Tabela de Preços")
st.markdown("Gerencie seus itens adicionando ou alterando preços direto pelo seu aplicativo do Google Sheets. O site atualizará automaticamente na tela.")
st.divider()
# ==========================================
# EXIBIÇÃO DA TABELA COM BARRA DE PESQUISA RÁPIDA
# ==========================================
if df_produtos.empty:
    st.info("Nenhum produto cadastrado na aba 'Produtos' da sua planilha.")
else:
    # Campo de busca em tempo real para agilizar no balcão do caixa
    busca = st.text_input("🔍 Buscar Produto por Nome", placeholder="Digite o nome da mercadoria para consultar o preço...").strip().lower()
    
    if busca:
        df_exibir = df_produtos[df_produtos["Produto"].astype(str).str.lower().str.contains(busca)]
    else:
        df_exibir = df_produtos.copy()
        
    if df_exibir.empty:
        st.warning("Nenhum produto encontrado com esse nome.")
    else:
        # Mostra o catálogo na tela formatado como moeda com o visual padrão limpo
        st.dataframe(
            df_exibir,
            use_container_width=True,
            hide_index=True,
            column_config={
                "Produto": st.column_config.TextColumn("Descrição da Mercadoria"),
                "Preco": st.column_config.NumberColumn("Preço de Venda", format="R$ %.2f")
            }
        )

# ==========================================
# RODAPÉ COM INDICADOR NUMÉRICO REAL
# ==========================================
st.divider()
total_itens = len(df_produtos)
st.metric("Variedade de Itens Praticados", f"{total_itens} produtos")
st.divider()
st.caption("Portal da Vila • Tabelas de Preço")
