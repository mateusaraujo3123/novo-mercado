import streamlit as st
import pandas as pd
import requests

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
# GOOGLE SHEETS (CONEXÃO DIRETA SEM CHAVES)
# ==========================================
ID_PLANILHA = "1u_bK8xpagg6AzDG9Slij9kyAWaa71roChrhCYYqL7ow"

# URL de leitura rápida que pula o bloqueio de tokens do Google
URL_LEITURA = f"https://google.com{ID_PLANILHA}/gviz/tq?tqx=out:csv&sheet=Produtos"

def carregar_produtos():
    try:
        df = pd.read_csv(URL_LEITURA)
        if df.empty or "Produto" not in df.columns:
            return pd.DataFrame(columns=["Produto", "Preco"])
        df["Preco"] = pd.to_numeric(df["Preco"], errors="coerce").fillna(0.0)
        return df[["Produto", "Preco"]].dropna(subset=["Produto"])
    except:
        return pd.DataFrame(columns=["Produto", "Preco"])

def salvar_produtos(df):
    # Salva as alterações na memória local da sua sessão do caixa
    st.session_state.produtos = df
    st.toast("💡 Alterações salvas na sessão atual do seu navegador!")

@st.cache_data(ttl=5) # Mudando o TTL, o Streamlit limpa a memória travada na hora
def carregar_produtos():
    try:
        # Garanta que a linha abaixo esteja escrita exatamente assim:
        df = pd.read_csv(URL_LEITURA)
        
        if df.empty or "Produto" not in df.columns:
            return pd.DataFrame(columns=["Produto", "Preco"])
            
        df["Preco"] = pd.to_numeric(df["Preco"], errors="coerce").fillna(0.0)
        return df[["Produto", "Preco"]].dropna(subset=["Produto"])
    except:
        return pd.DataFrame(columns=["Produto", "Preco"])
        
# ==========================================
# CARREGAR PRODUTOS (TTL DE 60s PARA ESTABILIDADE)
# ==========================================
@st.cache_data(ttl=60)
def carregar_produtos():
    dados = aba_produtos.get_all_records()
    if len(dados) == 0:
        return pd.DataFrame(columns=["Produto", "Preco"])
    
    df = pd.DataFrame(dados)
    colunas = ["Produto", "Preco"]
    
    for coluna in colunas:
        if coluna not in df.columns:
            df[coluna] = ""
            
    return df[colunas]

# ==========================================
# SALVAR PLANILHA
# ==========================================
def salvar_produtos(df):
    dados = [df.columns.tolist()]
    dados.extend(df.values.tolist())
    aba_produtos.clear()
    aba_produtos.update(dados)
    carregar_produtos.clear()

# ==========================================
# SESSION STATE
# ==========================================
if "produtos" not in st.session_state:
    st.session_state.produtos = carregar_produtos()

# ==========================================
# TÍTULO E ABAS
# ==========================================
st.title("📦 Tabela de Preços")
st.divider()

aba_lista, aba_novo, aba_excluir = st.tabs(
    [
        "📋 Preços Praticados",
        "➕ Novo Produto",
        "❌ Remover Produto"
    ]
)
# ==========================================
# ABA - LISTA E ALTERAÇÃO DE PREÇOS
# ==========================================
with aba_lista:
    st.subheader("Catálogo de Produtos")
    if st.session_state.produtos.empty:
        st.info("Nenhum produto cadastrado na tabela de preços.")
    else:
        produtos_editados = st.data_editor(
            st.session_state.produtos, hide_index=True, use_container_width=True, num_rows="dynamic", key="editor_produtos",
            column_config={
                "Produto": st.column_config.TextColumn("Descrição da Mercadoria", required=True),
                "Preco": st.column_config.NumberColumn("Preço de Venda (R$)", min_value=0.0, step=0.50, format="R$ %.2f")
            }
        )
        col1, col2 = st.columns(2)
        with col1:
            if st.button("💾 Salvar Alterações", use_container_width=True, type="primary", key="btn_salvar_prod"):
                produtos_editados = produtos_editados.fillna("")
                salvar_produtos(produtos_editados)
                st.session_state.produtos = carregar_produtos()
                st.success("Tabela de preços actualizada com sucesso!")
                st.rerun()
        with col2:
            if st.button("🔄 Atualizar Lista", use_container_width=True, key="btn_att_prod"):
                st.session_state.produtos = carregar_produtos()
                st.rerun()

# ==========================================
# ABA - CADASTRO DE NOVO PRODUTO
# ==========================================
with aba_novo:
    st.subheader("Cadastrar Novo Item")
    with st.form("novo_produto", clear_on_submit=True):
        nome_prod = st.text_input("Descrição / Nome do Produto")
        preco_venda = st.number_input("Preço de Venda Inicial (R$)", min_value=0.0, value=5.0, step=1.0)
        enviar_prod = st.form_submit_button("Cadastrar", type="primary")

    if enviar_prod:
        nome_prod = nome_prod.strip()
        if nome_prod == "":
            st.error("Informe a descrição do produto.")
        else:
            df_prod = carregar_produtos()
            itens_cadastrados = df_prod["Produto"].astype(str).str.strip().str.lower()
            if nome_prod.lower() in itens_cadastrados.values:
                st.error("Esta mercadoria já está cadastrada na tabela de preços.")
            else:
                nova_linha_prod = pd.DataFrame([{"Produto": nome_prod, "Preco": preco_venda}])
                df_prod = pd.concat([df_prod, nova_linha_prod], ignore_index=True)
                salvar_produtos(df_prod)
                st.session_state.produtos = carregar_produtos()
                st.success(f"'{nome_prod}' adicionado com sucesso!")
                st.rerun()

# ==========================================
# ABA - REMOVER PRODUTO
# ==========================================
with aba_excluir:
    st.subheader("Excluir Item do Catálogo")
    df_prod_atual = carregar_produtos()
    if df_prod_atual.empty:
        st.info("Nenhum produto cadastrado para remover.")
    else:
        with st.form("form_remover_produto"):
            lista_itens = df_prod_atual["Produto"].tolist()
            item_remover = st.selectbox("Selecione o produto que deseja apagar permanentemente:", lista_itens)
            st.error("⚠️ Atenção: O item será deletado definitivamente da tabela de preços.")
            caixa_confirmacaop = st.checkbox(f"Confirmo que desejo deletar o produto: {item_remover}")
            botao_deletarp = st.form_submit_button("Excluir Definitivamente", type="primary")

        if botao_deletarp:
            if not caixa_confirmacaop:
                st.error("Marque a caixa de confirmação para poder excluir.")
            else:
                df_filtrado_p = df_prod_atual[df_prod_atual["Produto"] != item_remover]
                salvar_produtos(df_filtrado_p)
                st.session_state.produtos = carregar_produtos()
                st.success(f"💥 '{item_remover}' foi removido do catálogo!")
                st.rerun()

# ==========================================
# RODAPÉ
# ==========================================
st.divider()
total_itens = len(st.session_state.produtos)
st.metric("Variedade de Itens Praticados", f"{total_itens} produtos")
st.divider()
st.caption("Portal da Vila • Tabelas de Preço")
