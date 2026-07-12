import streamlit as st
from streamlit_gsheets import GSheetsConnection
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

# Estabelece a conexão segura com a sua Planilha Google
conn = st.connection("gsheets", type=GSheetsConnection)

# Função para buscar os dados atualizados da planilha
def carregar_dados_reais():
    # Lê a aba 'Página1' conforme configurado na sua planilha original
    return conn.read(worksheet="Página1", ttl=0)

df_clientes = carregar_dados_reais()

# Garante que a tabela não venha nula ou sem colunas
if df_clientes.empty or "Nome" not in df_clientes.columns:
    df_clientes = pd.DataFrame(columns=["Nome", "Limite", "Divida"])

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
    # Limpa linhas completamente vazias da planilha para exibição limpa
    df_exibir = df_clientes.dropna(subset=["Nome"])
    
    if df_exibir.empty:
        st.info("Nenhum cliente cadastrado na planilha na nuvem.")
    else:
        st.dataframe(df_exibir, use_container_width=True, hide_index=True)

# --- SUBPASTA 2: CADASTRO DE NOVO CLIENTE ---
with aba_cadastro:
    st.subheader("Formulário de Cadastro")
    
    col_cad1, col_cad2 = st.columns(2)
    with col_cad1:
        nome_cliente = st.text_input("Nome Completo do Cliente", placeholder="Ex: João Silva").strip()
    with col_cad2:
        limite_credito = st.number_input("Limite Máximo de Fiado (R$)", min_value=0.0, value=200.0, step=50.0)
    
    if st.button("Salvar Cadastro", type="primary"):
        if nome_cliente:
            if nome_cliente in df_clientes["Nome"].values:
                st.error("⚠️ Este cliente já está cadastrado!")
            else:
                # Cria a nova linha com dívida inicial zerada
                novo_registro = pd.DataFrame([{"Nome": nome_cliente, "Limite": limite_credito, "Divida": 0.0}])
                df_atualizado = pd.concat([df_clientes, novo_registro], ignore_index=True)
                
                # Salva direto na sua planilha do Google Drive
                conn.update(worksheet="Página1", data=df_atualizado)
                st.success(f"✅ Cliente '{nome_cliente}' gravado com sucesso na nuvem!")
                st.rerun()
        else:
            st.error("⚠️ Por favor, digite o nome do cliente antes de salvar.")

# --- SUBPASTA 3: REGISTRAR PAGAMENTO ---
with aba_recebimento:
    st.subheader("Dar Baixa em Dívida")
    df_filtrado = df_clientes.dropna(subset=["Nome"])
    
    if df_filtrado.empty:
        st.info("Nenhum cliente disponível para receber.")
    else:
        lista_nomes = df_filtrado["Nome"].tolist()
        col_pago1, col_pago2 = st.columns(2)
        with col_pago1:
            cliente_selecionado = st.selectbox("Selecione o Cliente:", lista_nomes)
        with col_pago2:
            valor_pago = st.number_input("Valor Pago (R$)", min_value=0.0, step=10.0)
            
        if st.button("Confirmar Recebimento"):
            if valor_pago > 0:
                # Atualiza a dívida subtraindo o valor pago
                df_clientes.loc[df_clientes["Nome"] == cliente_selecionado, "Divida"] -= valor_pago
                conn.update(worksheet="Página1", data=df_clientes)
                st.success(f"✅ Pagamento de R$ {valor_pago:.2f} registrado! Planilha atualizada.")
                st.rerun()
            else:
                st.error("⚠️ Digite um valor maior que zero para o pagamento.")

# --- SUBPASTA 4: REMOVER CLIENTE ---
with aba_remover:
    st.subheader("❌ Excluir Cliente do Sistema")
    df_filtrado_rem = df_clientes.dropna(subset=["Nome"])
    
    if df_filtrado_rem.empty:
        st.info("Nenhum cliente na lista para remoção.")
    else:
        lista_nomes_remover = df_filtrado_rem["Nome"].tolist()
        cliente_para_remover = st.selectbox("Escolha o cliente que deseja apagar:", lista_nomes_remover, key="sb_remover")
        confirmou = st.checkbox(f"Confirmo que desejo apagar permanentemente o cadastro de '{cliente_para_remover}'")
        
        if st.button("Excluir Cadastro Definitivamente", type="secondary"):
            if confirmou:
                # Remove a linha correspondente ao cliente selecionado
                df_atualizado = df_clientes[df_clientes["Nome"] != cliente_para_remover]
                conn.update(worksheet="Página1", data=df_atualizado)
                st.success(f"💥 O cadastro de '{cliente_para_remover}' foi apagado da planilha!")
                st.rerun()
            else:
                st.error("⚠️ Você precisa marcar a caixa de confirmação antes de excluir.")
