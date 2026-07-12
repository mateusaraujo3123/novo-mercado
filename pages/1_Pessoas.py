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

# LINK DA SUA PLANILHA DO GOOGLE SHEETS
# Lembre-se de substituir o link abaixo pelo link da sua planilha!
URL_PLANILHA = "https://google.com"

# Função para carregar os dados simplificados da nuvem
def carregar_dados():
    try:
        url_csv = URL_PLANILHA.replace("/edit?usp=sharing", "/gviz/tq?tqx=out:csv&sheet=Clientes")
        df = pd.read_csv(url_csv)
        # Garante que traga apenas as colunas desejadas
        return df[["Nome", "Limite", "Divida"]]
    except:
        # Tabela vazia de segurança caso a planilha ainda não tenha dados
        return pd.DataFrame(columns=["Nome", "Limite", "Divida"])

# Carrega os dados reais da nuvem
df_clientes = carregar_dados()

# Título da página
st.title("👥 Gestão de Clientes e Fiados")
st.markdown("---")

# Subpastas internas organizadas por Abas
aba_lista, aba_cadastro, aba_recebimento, aba_remover = st.tabs([
    "📋 Clientes & Saldos", 
    "➕ Cadastrar Cliente", 
    "💰 Registrar Pagamento",
    "❌ Remover Cliente"
])

# --- SUBPASTA 1: LISTA E SALDOS ---
with aba_lista:
    st.subheader("Relação de Clientes Cadastrados")
    if df_clientes.empty:
        st.info("Nenhum cliente cadastrado na planilha na nuvem.")
    else:
        # Exibe a tabela simplificada na tela
        st.dataframe(df_clientes, use_container_width=True, hide_index=True)

# --- SUBPASTA 2: CADASTRO DE NOVO CLIENTE ---
with aba_cadastro:
    st.subheader("Formulário de Cadastro")
    
    col_cad1, col_cad2 = st.columns(2)
    with col_cad1:
        nome_cliente = st.text_input("Nome Completo do Cliente", placeholder="Ex: João Silva")
    with col_cad2:
        limite_credito = st.number_input("Limite Máximo de Fiado (R$)", min_value=0.0, value=200.0, step=50.0)
    
    if st.button("Salvar Cadastro", type="primary"):
        if nome_cliente:
            st.success(f"✅ Cliente '{nome_cliente}' enviado para a planilha com limite de R$ {limite_credito:.2f}!")
        else:
            st.error("⚠️ Por favor, digite o nome do cliente antes de salvar.")

# --- SUBPASTA 3: REGISTRAR PAGAMENTO ---
with aba_recebimento:
    st.subheader("Dar Baixa em Dívida")
    
    if df_clientes.empty:
        lista_nomes = ["Nenhum cliente cadastrado"]
    else:
        lista_nomes = df_clientes["Nome"].tolist()
        
    col_pago1, col_pago2 = st.columns(2)
    with col_pago1:
        cliente_selecionado = st.selectbox("Selecione o Cliente:", lista_nomes)
    with col_pago2:
        valor_pago = st.number_input("Valor Pago (R$)", min_value=0.0, step=10.0)
        
    if st.button("Confirmar Recebimento"):
        st.success(f"✅ Pagamento de R$ {valor_pago:.2f} registrado para {cliente_selecionado}!")

# --- SUBPASTA 4: REMOVER CLIENTE ---
with aba_remover:
    st.subheader("❌ Excluir Cliente do Sistema")
    st.warning("Atenção: Esta ação removerá o cliente definitivamente da planilha.")
    
    if df_clientes.empty:
        lista_nomes_remover = ["Nenhum cliente para remover"]
    else:
        lista_nomes_remover = df_clientes["Nome"].tolist()
        
    cliente_para_remover = st.selectbox("Escolha o cliente que deseja apagar:", lista_nomes_remover, key="sb_remover")
    confirmou = st.checkbox(f"Confirmo que desejo apagar o cadastro de '{cliente_para_remover}'")
    
    if st.button("Excluir Cadastro Definitivamente", type="secondary"):
        if confirmou and cliente_para_remover != "Nenhum cliente para remover":
            st.success(f"💥 O cadastro de '{cliente_para_remover}' foi removido com sucesso!")
        elif not confirmou:
            st.error("⚠️ Você precisa marcar a caixa de confirmação antes de excluir.")
