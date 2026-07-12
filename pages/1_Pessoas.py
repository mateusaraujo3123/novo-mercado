import streamlit as st
import pandas as pd

# Configuração da página
st.set_page_config(
    page_title="Gestão de Fiados - Portal Da Vila",
    page_icon="👥",
    layout="wide"
)

# REINTEGRAÇÃO DO MENU LATERAL
st.sidebar.markdown("# 🏪 Menu Mercadinho")
st.sidebar.write("Ir para:")
st.sidebar.radio(
    "Navegação", 
    ["Dashboard Inicial", "Gestão de Fiados", "Tabelas de Preço"], 
    index=1,
    label_visibility="collapsed"
)

# ID público estável da sua planilha fornecida
ID_PLANILHA = "1u_bK8xpagg6AzDG9Slij9kyAWaa71roChrhCYYqL7ow"
URL_CSV = f"https://google.com{ID_PLANILHA}/gviz/tq?tqx=out:csv&sheet=clientes"

# Carrega os dados reais do Google Sheets de forma limpa via pandas
@st.cache_data(ttl=5) # Atualiza o cachê a cada 5 segundos se houver mudança
def buscar_dados_google():
    try:
        df = pd.read_csv(URL_CSV)
        if df.empty or "Nome" not in df.columns:
            return pd.DataFrame(columns=["Nome", "Limite", "Divida"])
        return df[["Nome", "Limite", "Divida"]].dropna(subset=["Nome"])
    except:
        return pd.DataFrame(columns=["Nome", "Limite", "Divida"])

# Inicializa os dados reais na sessão para edição dinâmica
if "banco_clientes" not in st.session_state:
    st.session_state.banco_clientes = buscar_dados_google()

# Título da página
st.title("👥 Gestão de Clientes e Fiados")
st.markdown("---")

# Subpastas internas organizadas de forma otimizada em 2 abas
aba_lista, aba_acoes = st.tabs([
    "📋 Painel de Controle (Editar/Remover)", 
    "➕ Novo Cadastro Rápido"
])

# --- ABA 1: PAINEL DE CONTROLE INTEGRADO ---
with aba_lista:
    st.subheader("Gerenciamento Geral de Fiados")
    st.markdown("💡 *Dica: Você pode dar baixa em pagamentos, alterar limites ou remover linhas diretamente na tabela abaixo!*")
    
    if st.session_state.banco_clientes.empty:
        st.info("Nenhum registro ativo puxado da nuvem. Cadastre o primeiro cliente na aba ao lado.")
    else:
        # Gera a planilha interativa na tela com edição e exclusão integradas de forma nativa
        dados_editados = st.data_editor(
            st.session_state.banco_clientes,
            use_container_width=True,
            num_rows="dynamic", # Permite que você clique em linhas e aperte 'Delete' para remover clientes
            column_config={
                "Nome": st.column_config.TextColumn("Nome Completo", required=True),
                "Limite": st.column_config.NumberColumn("Limite Máximo (R$)", min_value=0, format="R$ %d"),
                "Divida": st.column_config.NumberColumn("Dívida Atual (R$)", min_value=0, format="R$ %.2f"),
            },
            key="editor_clientes"
        )
        
        # Botão para validar as alterações em lote
        if st.button("Salvar Alterações no Banco", type="primary"):
            st.session_state.banco_clientes = dados_editados
            st.success("🎉 Alterações gravadas localmente com sucesso no sistema!")
            st.rerun()

# --- ABA 2: NOVO CADASTRO RÁPIDO ---
with aba_acoes:
    st.subheader("Cadastrar Cliente no Sistema")
    
    with st.form("form_cadastro_cliente", clear_on_submit=True):
        col_cad1, col_cad2 = st.columns(2)
        with col_cad1:
            novo_nome = st.text_input("Nome Completo do Cliente", placeholder="Ex: João Silva").strip()
        with col_cad2:
            novo_limite = st.number_input("Limite de Fiado Inicial (R$)", min_value=0.0, value=200.0, step=50.0)
            
        submit = st.form_submit_button("Registrar na Base", type="primary")
        
        if submit:
            if novo_nome:
                if novo_nome in st.session_state.banco_clientes["Nome"].astype(str).values:
                    st.error("⚠️ Este cliente já consta na lista cadastrada!")
                else:
                    # Injeta a linha com dívida zero na tabela atualizada
                    nova_linha = pd.DataFrame([{"Nome": novo_nome, "Limite": novo_limite, "Divida": 0.0}])
                    st.session_state.banco_clientes = pd.concat([st.session_state.banco_clientes, nova_linha], ignore_index=True)
                    st.success(f"✅ Cliente '{novo_nome}' adicionado! Vá à aba de controle e clique em Salvar.")
                    st.rerun()
            else:
                st.error("⚠️ Insira um nome válido antes de confirmar.")
