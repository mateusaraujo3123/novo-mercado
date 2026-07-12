import streamlit as st
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials


# ==========================================
# CONFIGURAÇÃO DA PÁGINA
# ==========================================

st.set_page_config(
    page_title="Gestão de Fiados - Portal da Vila",
    page_icon="🏪",
    layout="wide"
)


# ==========================================
# MENU LATERAL
# ==========================================

st.sidebar.title("🏪 Portal da Vila")

pagina = st.sidebar.radio(
    "Menu",
    [
        "Dashboard",
        "Gestão de Fiados"
    ]
)


# ==========================================
# GOOGLE SHEETS
# ==========================================

ID_PLANILHA = "1u_bK8xpagg6AzDG9Slij9kyAWaa71roChrhCYYqL7ow"


SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]


@st.cache_resource
def conectar_planilha():

    credenciais = Credentials.from_service_account_info(
        st.secrets["gcp_service_account"],
        scopes=SCOPES
    )

    cliente = gspread.authorize(
        credenciais
    )

    return cliente.open_by_key(
        ID_PLANILHA
    )


planilha = conectar_planilha()

aba_clientes = planilha.worksheet("Clientes")



# ==========================================
# CARREGAR CLIENTES
# ==========================================

@st.cache_data(ttl=10)
def carregar_clientes():

    dados = aba_clientes.get_all_records()


    if not dados:

        return pd.DataFrame(
            columns=[
                "Nome",
                "Limite",
                "Divida"
            ]
        )


    df = pd.DataFrame(dados)


    for coluna in [
        "Nome",
        "Limite",
        "Divida"
    ]:

        if coluna not in df.columns:
            df[coluna] = 0


    df["Limite"] = pd.to_numeric(
        df["Limite"],
        errors="coerce"
    ).fillna(0)


    df["Divida"] = pd.to_numeric(
        df["Divida"],
        errors="coerce"
    ).fillna(0)


    return df[
        [
            "Nome",
            "Limite",
            "Divida"
        ]
    ]



# ==========================================
# SALVAR
# ==========================================

def salvar_clientes(df):

    dados = [
        df.columns.tolist()
    ]

    dados += df.values.tolist()


    aba_clientes.clear()

    aba_clientes.update(
        dados
    )


    carregar_clientes.clear()

# ==========================================
# GESTÃO DE FIADOS
# ==========================================

if pagina == "Gestão de Fiados":

    st.title("👥 Gestão de Clientes")

    df_clientes = carregar_clientes()


    aba_lista, aba_novo, aba_compra, aba_pagamento, aba_excluir = st.tabs(
        [
            "📋 Clientes",
            "➕ Novo Cliente",
            "🛒 Adicionar Compra",
            "💰 Receber Pagamento",
            "❌ Excluir Cliente"
        ]
    )


    # ==========================================
    # LISTA DE CLIENTES
    # ==========================================

    with aba_lista:

        st.subheader("Clientes Cadastrados")


        if df_clientes.empty:

            st.info("Nenhum cliente cadastrado.")

        else:

            editado = st.data_editor(
                df_clientes,
                hide_index=True,
                use_container_width=True,
                column_config={

                    "Nome": st.column_config.TextColumn(
                        "Nome"
                    ),

                    "Limite": st.column_config.NumberColumn(
                        "Limite (R$)",
                        format="R$ %.2f"
                    ),

                    "Divida": st.column_config.NumberColumn(
                        "Dívida (R$)",
                        format="R$ %.2f"
                    )
                }
            )


            if st.button(
                "💾 Salvar Alterações",
                type="primary"
            ):

                salvar_clientes(editado)

                st.success(
                    "Dados atualizados!"
                )

                st.rerun()



    # ==========================================
    # NOVO CLIENTE
    # ==========================================

    with aba_novo:

        st.subheader(
            "Cadastrar Cliente"
        )


        with st.form(
            "novo_cliente"
        ):

            nome = st.text_input(
                "Nome"
            )

            limite = st.number_input(
                "Limite de Fiado",
                min_value=0.0,
                value=200.0
            )


            salvar = st.form_submit_button(
                "Cadastrar"
            )


        if salvar:


            if nome.strip() == "":

                st.error(
                    "Digite o nome do cliente."
                )

            else:

                df = carregar_clientes()


                existe = (
                    df["Nome"]
                    .astype(str)
                    .str.lower()
                    .eq(nome.lower())
                    .any()
                )


                if existe:

                    st.error(
                        "Cliente já cadastrado."
                    )

                else:

                    novo = pd.DataFrame(
                        [
                            {
                                "Nome": nome,
                                "Limite": limite,
                                "Divida": 0
                            }
                        ]
                    )


                    df = pd.concat(
                        [
                            df,
                            novo
                        ],
                        ignore_index=True
                    )


                    salvar_clientes(df)


                    st.success(
                        "Cliente cadastrado!"
                    )

                    st.rerun()



    # ==========================================
    # ADICIONAR COMPRA
    # ==========================================

    with aba_compra:

        st.subheader(
            "Adicionar Compra Fiada"
        )


        df = carregar_clientes()


        if df.empty:

            st.info(
                "Cadastre clientes primeiro."
            )

        else:


            cliente = st.selectbox(
                "Cliente",
                df["Nome"]
            )


            valor = st.number_input(
                "Valor da compra",
                min_value=0.01,
                step=5.0
            )


            if st.button(
                "Confirmar Compra"
            ):


                df.loc[
                    df["Nome"] == cliente,
                    "Divida"
                ] += valor


                salvar_clientes(df)


                st.success(
                    "Compra adicionada!"
                )

                st.rerun()



    # ==========================================
    # PAGAMENTO
    # ==========================================

    with aba_pagamento:

        st.subheader(
            "Receber Pagamento"
        )


        df = carregar_clientes()


        devedores = df[
            df["Divida"] > 0
        ]


        if devedores.empty:

            st.info(
                "Nenhum cliente devendo."
            )

        else:


            cliente = st.selectbox(
                "Cliente",
                devedores["Nome"]
            )


            divida = float(
                devedores[
                    devedores["Nome"] == cliente
                ]["Divida"].iloc[0]
            )


            pagamento = st.number_input(
                "Valor pago",
                min_value=0.01,
                max_value=divida,
                value=divida
            )


            if st.button(
                "Confirmar Pagamento"
            ):


                df.loc[
                    df["Nome"] == cliente,
                    "Divida"
                ] -= pagamento


                salvar_clientes(df)


                st.success(
                    "Pagamento registrado!"
                )

                st.rerun()

    # ==========================================
    # EXCLUIR CLIENTE
    # ==========================================

    with aba_excluir:

        st.subheader(
            "Excluir Cliente"
        )


        df = carregar_clientes()


        if df.empty:

            st.info(
                "Não existem clientes cadastrados."
            )

        else:


            cliente = st.selectbox(
                "Escolha o cliente para excluir",
                df["Nome"]
            )


            confirmar = st.checkbox(
                "Confirmo que desejo excluir este cliente"
            )


            if st.button(
                "❌ Excluir Cliente",
                type="primary"
            ):


                if confirmar:


                    df = df[
                        df["Nome"] != cliente
                    ]


                    salvar_clientes(df)


                    st.success(
                        "Cliente removido!"
                    )

                    st.rerun()


                else:

                    st.warning(
                        "Marque a confirmação primeiro."
                    )



# ==========================================
# DASHBOARD
# ==========================================

if pagina == "Dashboard":


    st.title(
        "📊 Dashboard - Portal da Vila"
    )


    df = carregar_clientes()


    total_clientes = len(df)


    total_divida = df["Divida"].sum()


    total_limite = df["Limite"].sum()



    col1, col2, col3 = st.columns(3)


    with col1:

        st.metric(
            "👥 Clientes",
            total_clientes
        )


    with col2:

        st.metric(
            "💰 Total Fiado",
            f"R$ {total_divida:,.2f}"
        )


    with col3:

        st.metric(
            "📌 Limite Total",
            f"R$ {total_limite:,.2f}"
        )



    st.divider()



    # ==========================================
    # GRÁFICO DOS MAIORES DEVEDORES
    # ==========================================

    st.subheader(
        "🏆 Maiores Devedores"
    )


    ranking = df.copy()


    ranking = ranking[
        ranking["Divida"] > 0
    ]


    ranking = ranking.sort_values(
        "Divida",
        ascending=False
    )


    if ranking.empty:


        st.info(
            "Nenhum fiado registrado."
        )


    else:


        st.dataframe(
            ranking[
                [
                    "Nome",
                    "Divida"
                ]
            ],
            hide_index=True,
            use_container_width=True
        )


        grafico = ranking.set_index(
            "Nome"
        )[
            [
                "Divida"
            ]
        ]


        st.bar_chart(
            grafico,
            use_container_width=True
        )



st.divider()


st.caption(
    "Portal da Vila • Sistema de Gestão de Fiados"
)
