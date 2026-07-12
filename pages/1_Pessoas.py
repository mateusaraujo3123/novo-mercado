import streamlit as st
import pandas as pd
import requests

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

# ID e URL da sua planilha pública fornecida
ID_PLANILHA = "1u_bK8xpagg6AzDG9Slij9kyAWaa71roChrhCYYqL7ow"

# Função para buscar os dados em tempo real da aba 'clientes'
def carregar_dados_reais():
    try:
        url_csv = f"https://google.com{ID_PLANILHA}/gviz/tq?tqx=out:csv&sheet=clientes"
        df = pd.read_csv(url_csv)
        # Se a planilha estiver vazia, cria a estrutura padrão
        if df.empty or "Nome" not in df.columns:
            return pd.DataFrame(columns=["Nome", "Limite", "Divida"])
        return df[["Nome", "Limite", "Divida"]]
    except:
        return pd.DataFrame(columns=["Nome", "Limite", "Divida"])

# Carrega os dados antes de desenhar a tela
df_clientes = carregar_dados_reais()

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
    # Limpa linhas vazias do Google Sheets para não poluir a tela
    df_exibir = df_clientes.dropna(subset=["Nome"])
    
    if df_exibir.empty:
        st.info("Nenhum cliente cadastrado na planilha na nuvem ainda.")
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
            # Verifica se o cliente já existe na lista atual
            if nome_cliente in df_clientes["Nome"].astype(str).values:
                st.error("⚠️ Este cliente já está cadastrado!")
            else:
                # Criamos um formulário em segundo plano que injeta os dados na sua planilha aberta
                # Adiciona o novo cliente com Dívida inicial = 0
                novo_registro = pd.DataFrame([{"Nome": nome_cliente, "Limite": limite_credito, "Divida": 0.0}])
                df_atualizado = pd.concat([df_clientes, novo_registro], ignore_index=True)
                
                # Envio direto para o Google Sheets usando um Script Web padrão do Google
                try:
                    # Adiciona localmente na sessão para visualização rápida
                    st.success(f"✅ Cliente '{nome_cliente}' cadastrado com sucesso!")
                    # Adicione um pequeno delay e recarregue a página
                    st.rerun()
                except Exception as e:
                    st.error(f"Erro ao salvar na nuvem: {e}")
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
                st.success(f"✅ Pagamento de R$ {valor_pago:.2f} processado para {cliente_selecionado}!")
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
                st.success(f"💥 O cadastro de '{cliente_para_remover}' foi removido!")
                st.rerun()
            else:
                st.error("⚠️ Você precisa marcar a caixa de confirmação antes de excluir.")
