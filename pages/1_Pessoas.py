import streamlit as st
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials

# ==========================================
# CONFIGURAÇÃO DA PÁGINA
# ==========================================

st.set_page_config(
    page_title="Gestão de Fiados - Portal da Vila",
    page_icon="👥",
    layout="wide"
)

# ==========================================
# MENU LATERAL
# ==========================================

st.sidebar.markdown("# 🏪 Menu Mercadinho")

st.sidebar.radio(
    "Navegação",
    [
        "Dashboard Inicial",
        "Gestão de Fiados",
        "Tabelas de Preço"
    ],
    index=1,
    label_visibility="collapsed"
)

# ==========================================
# GOOGLE SHEETS
# ==========================================

ID_PLANILHA = "1u_bK8xpagg6AzDG9Slij9kyAWaa71roChrhCYYqL7ow"

SCOPES = [
    "https://googleapis.com",
    "https://googleapis.com"
]


@st.cache_resource
def conectar_planilha():

    creds = Credentials.from_service_account_info(
        st.secrets["gcp_service_account"],
        scopes=SCOPES
    )

    cliente = gspread.authorize(creds)

    planilha = cliente.open_by_key(ID_PLANILHA)

    return planilha


planilha = conectar_planilha()

aba_clientes = planilha.worksheet("Clientes")

# ==========================================
# CARREGAR CLIENTES
# ==========================================

@st.cache_data(ttl=5)
def carregar_clientes():

    dados = aba_clientes.get_all_records()

    if len(dados) == 0:

        return pd.DataFrame(
            columns=[
                "Nome",
                "Limite",
                "Divida"
            ]
        )

    df = pd.DataFrame(dados)

    colunas = ["Nome", "Limite", "Divida"]

    for coluna in colunas:

        if coluna not in df.columns:

            df[coluna] = ""

    return df[colunas]

# ==========================================
# SALVAR PLANILHA
# ==========================================

def salvar_clientes(df):

    dados = [df.columns.tolist()]

    dados.extend(df.values.tolist())

    aba_clientes.clear()

    aba_clientes.update(dados)

    carregar_clientes.clear()

# ==========================================
# SESSION STATE
# ==========================================

if "clientes" not in st.session_state:

    st.session_state.clientes = carregar_clientes()

# ==========================================
# TÍTULO
# ==========================================

st.title("👥 Gestão de Clientes")

st.divider()

aba_lista, aba_novo, aba_adicionar, aba_abater, aba_excluir = st.tabs(
    [
        "📋 Clientes",
        "➕ Novo Cliente",
        "✍️ Adicionar Compra",
        "💰 Receber Pagamento",
        "❌ Remover Cliente"
    ]
)
# ==========================================
# ABA - CLIENTES
# ==========================================

with aba_lista:

    st.subheader("Clientes Cadastrados")

    if st.session_state.clientes.empty:

        st.info("Nenhum cliente cadastrado.")

    else:

        clientes_editados = st.data_editor(

            st.session_state.clientes,

            hide_index=True,

            use_container_width=True,

            num_rows="dynamic",

            key="editor_clientes",

            column_config={

                "Nome": st.column_config.TextColumn(

                    "Nome",

                    required=True

                ),

                "Limite": st.column_config.NumberColumn(

                    "Limite (R$)",

                    min_value=0,

                    step=10,

                    format="R$ %.2f"

                ),

                "Divida": st.column_config.NumberColumn(

                    "Dívida (R$)",

                    min_value=0,

                    step=1,

                    format="R$ %.2f"

                )

            }

        )

        col1, col2 = st.columns(2)

        with col1:

            if st.button(

                "💾 Salvar Alterações",

                use_container_width=True,

                type="primary"

            ):

                clientes_editados = clientes_editados.fillna("")

                salvar_clientes(clientes_editados)

                st.session_state.clientes = carregar_clientes()

                st.success("Clientes atualizados com sucesso!")

                st.rerun()

        with col2:

            if st.button(

                "🔄 Atualizar Lista",

                use_container_width=True

            ):

                st.session_state.clientes = carregar_clientes()

                st.rerun()

        # ==========================================
        # SEÇÃO DO GRÁFICO DE DEVEDORES
        # ==========================================
        st.write("")
        st.subheader("📊 Gráfico de Maiores Devedores")
        
        df_grafico = st.session_state.clientes.copy()
        df_grafico["Divida"] = pd.to_numeric(df_grafico["Divida"], errors="coerce").fillna(0.0)
        df_grafico = df_grafico[df_grafico["Divida"] > 0].sort_values(by="Divida", ascending=True)

        if df_grafico.empty:
            st.info("Nenhum cliente com dívida ativa para exibir no gráfico.")
        else:
            df_chart_data = df_grafico.set_index("Nome")[["Divida"]]
            st.bar_chart(df_chart_data, horizontal=True, use_container_width=True)

# ==========================================
# ABA - NOVO CLIENTE
# ==========================================

with aba_novo:

    st.subheader("Cadastrar Novo Cliente")

    with st.form("novo_cliente", clear_on_submit=True):

        nome = st.text_input(
            "Nome do Cliente"
        )

        limite = st.number_input(
            "Limite de Fiado",
            min_value=0.0,
            value=200.0,
            step=50.0
        )

        enviar = st.form_submit_button(
            "Cadastrar",
            type="primary"
        )

    if enviar:

        nome = nome.strip()

        if nome == "":

            st.error("Informe o nome do cliente.")

        else:

            df = carregar_clientes()

            nomes = (
                df["Nome"]
                .astype(str)
                .str.strip()
                .str.lower()
            )

            if nome.lower() in nomes.values:

                st.error("Este cliente já está cadastrado.")

            else:

                nova_linha = pd.DataFrame([
                    {
                        "Nome": nome,
                        "Limite": limite,
                        "Divida": 0.0
                    }
                ])

                df = pd.concat(
                    [df, nova_linha],
                    ignore_index=True
                )

                salvar_clientes(df)

                st.session_state.clientes = carregar_clientes()

                st.success(f"{nome} cadastrado com sucesso!")

                st.rerun()

# ==========================================
# ABA - ADICIONAR COMPRA (AUMENTAR DÍVIDA)
# ==========================================

with aba_adicionar:

    st.subheader("Registrar Nova Compra no Fiado")

    df_atual = carregar_clientes()

    if df_atual.empty:

        st.info("Nenhum cliente cadastrado.")

    else:

        with st.form("form_adicionar_compra", clear_on_submit=True):

            lista_clientes = df_atual["Nome"].tolist()
            
            cliente_comprando = st.selectbox(
                "Selecione o Cliente que está comprando:",
                lista_clientes
            )

            # Correção com .iloc[0] para extrair o valor de forma segura
            linha_cliente = df_atual[df_atual["Nome"] == cliente_comprando]
            divida_atual = float(pd.to_numeric(linha_cliente["Divida"], errors="coerce").fillna(0.0).iloc[0])
            limite_atual = float(pd.to_numeric(linha_cliente["Limite"], errors="coerce").fillna(0.0).iloc[0])
            disponivel = max(0.0, limite_atual - divida_atual)

            st.info(f"Dívida Atual: R$ {divida_atual:,.2f} | Limite: R$ {limite_atual:,.2f} | Disponível: R$ {disponivel:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))

            valor_compra = st.number_input(
                "Valor da Nova Compra (R$)",
                min_value=0.01,
                value=10.0,
                step=5.0
            )

            confirmar_compra = st.form_submit_button(
                "Confirmar Nova Compra",
                type="primary"
            )

        if confirmar_compra:

            df_atual.loc[df_atual["Nome"] == cliente_comprando, "Divida"] = divida_atual + valor_compra
            
            salvar_clientes(df_atual)

            st.session_state.clientes = carregar_clientes()

            st.success(f"✅ R$ {valor_compra:,.2f} adicionados à conta de {cliente_comprando} com sucesso!".replace(",", "X").replace(".", ",").replace("X", "."))

            st.rerun()

# ==========================================
# ABA - RECEBER PAGAMENTO (ABATER DÍVIDA)
# ==========================================

with aba_abater:

    st.subheader("Registrar Pagamento de Cliente")

    df_atual = carregar_clientes()
    df_devedores = df_atual[pd.to_numeric(df_atual["Divida"], errors="coerce").fillna(0) > 0]

    if df_devedores.empty:

        st.info("Nenhum cliente possui dívidas pendentes no momento.")

    else:

        with st.form("form_abater_divida", clear_on_submit=True):

            lista_devedores = df_devedores["Nome"].tolist()
            
            cliente_pagando = st.selectbox(
                "Selecione o Cliente:",
                lista_devedores
            )

            # Correção com .iloc[0] para extrair o valor de forma segura
            linha_devedor = df_devedores[df_devedores["Nome"] == cliente_pagando]
            divida_atual = float(pd.to_numeric(linha_devedor["Divida"], errors="coerce").fillna(0.0).iloc[0])
            st.warning(f"Dívida Atual deste cliente: R$ {divida_atual:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))

            valor_pago = st.number_input(
                "Valor Pago (R$)",
                min_value=0.01,
                max_value=divida_atual,
                value=divida_atual,
                step=5.0
            )

            confirmar_pagamento = st.form_submit_button(
                "Confirmar Recebimento",
                type="primary"
            )

        if confirmar_pagamento:

            df_atual.loc[df_atual["Nome"] == cliente_pagando, "Divida"] = divida_atual - valor_pago
            
            salvar_clientes(df_atual)

            st.session_state.clientes = carregar_clientes()

            st.success(f"✅ R$ {valor_pago:,.2f} abatidos da conta de {cliente_pagando} com sucesso!".replace(",", "X").replace(".", ",").replace("X", "."))

            st.rerun()

# ==========================================
# ABA - REMOVER CLIENTE
# ==========================================

with aba_excluir:

    st.subheader("Excluir Cliente do Sistema")

    df_atual = carregar_clientes()

    if df_atual.empty:

        st.info("Nenhum cliente cadastrado para remover.")

    else:

        with st.form("form_remover_cliente"):

            lista_todos = df_atual["Nome"].tolist()

            cliente_remover = st.selectbox(
                "Selecione o cliente que deseja apagar permanentemente:",
                lista_todos
            )

            st.error("⚠️ Atenção: Esta ação não pode ser desfeita. O cliente será deletado da planilha.")

            caixa_confirmacao = st.checkbox(
                f"Confirmo que desejo deletar o cadastro de {cliente_remover}"
            )

            botao_deletar = st.form_submit_button(
                "Excluir Cadastro Definitivamente",
                type="primary"
            )

        if botao_deletar:

            if not caixa_confirmacao:

                st.error("Marque a caixa de confirmação para poder excluir.")

            else:

                df_filtrado = df_atual[df_atual["Nome"] != cliente_remover]

                salvar_clientes(df_filtrado)

                st.session_state.clientes = carregar_clientes()

                st.success(f"{cliente_remover} foi removido do sistema!")

                st.rerun()

# ==========================================
# RODAPÉ (ORGANIZADO NA ORDEM EXATA)
# ==========================================

st.divider()

total_clientes = len(st.session_state.clientes)

total_divida = (
    pd.to_numeric(
        st.session_state.clientes["Divida"],
        errors="coerce"
    )
    .fillna(0)
    .sum()
)

total_limite = (
    pd.to_numeric(
        st.session_state.clientes["Limite"],
        errors="coerce"
    )
    .fillna(0)
    .sum()
)

c1, c2, c3 = st.columns(3)

with c1:
