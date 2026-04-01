import streamlit as st
import pandas as pd
import os

# ---------------- ARQUIVOS ----------------
ARQ_LAVAGENS = "lavagens.csv"
ARQ_USUARIOS = "usuarios.csv"

# Link da imagem do Shrek
SHREK_URL = "https://i.pinimg.com/originals/f9/65/5a/f9655a045a4285693c9a2b48e2980c75.png"

# Criar arquivos se não existirem
if not os.path.exists(ARQ_LAVAGENS):
    pd.DataFrame(columns=["Funcionario", "Tipo Lavagem", "Data", "Dia", "Hora", "Pagamento"]).to_csv(ARQ_LAVAGENS, index=False)

if not os.path.exists(ARQ_USUARIOS):
    pd.DataFrame([{"usuario": "admin", "senha": "admin"}]).to_csv(ARQ_USUARIOS, index=False)

# ---------------- SESSÃO ----------------
if "logado" not in st.session_state:
    st.session_state.logado = False
if "tela" not in st.session_state:
    st.session_state.tela = "login"

# ---------------- CSS TEMA SHREK ----------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Creepster&display=swap');

body {background-color: #1f2e00;}
.stApp {background-color: #1f2e00; color: #FFFFFF; font-family: 'Creepster', cursive;}
h1, h2, h3 {color: #3c5e28; text-align: center; text-shadow: 2px 2px #d1e0a1;}
.stButton>button {background-color: #1f2e00; color: #f4f1c9; border-radius: 20px; height: 3em; width: 100%; font-weight: bold; font-size: 16px; box-shadow: 2px 2px 5px #556b2f;}
.stTextInput>div>div>input, .stSelectbox>div>div {border-radius: 15px; border: 2px solid #3c5e28; padding: 5px; background-color: #e1f0b3; color: #1b2f1b; font-weight: bold;}
.stDataFrame table {background-color: #1f2e00; color: #1b2f1b; border: 2px solid #3c5e28;}
::-webkit-scrollbar {width: 12px;}
::-webkit-scrollbar-track {background: #1f2e00;}
::-webkit-scrollbar-thumb {background-color:  #1f2e00; border-radius: 20px; border: 3px solid #cfe1a1;}
</style>
""", unsafe_allow_html=True)

# ---------------- FUNÇÕES ----------------
def mostrar_titulo_com_shrek(titulo):
    """Exibe o título com a imagem do Shrek ao lado"""
    col1, col2 = st.columns([3,8])
    with col1:
        st.image(SHREK_URL, width=150)  # imagem via URL
    with col2:
        st.title(titulo)

def tela_login():
    mostrar_titulo_com_shrek("Login do SHREK")
    usuario = st.text_input("Usuário")
    senha = st.text_input("Senha", type="password")

    if st.button("Entrar"):
        df = pd.read_csv(ARQ_USUARIOS)
        df["usuario"] = df["usuario"].astype(str).str.strip()
        df["senha"] = df["senha"].astype(str).str.strip()
        if any((df["usuario"].str.lower() == usuario.strip().lower()) & (df["senha"] == senha.strip())):
            st.session_state.logado = True
            st.success("Login realizado!")
            st.rerun()
        else:
            st.error("Usuário ou senha incorretos")

    if st.button("Ir para Cadastro"):
        st.session_state.tela = "cadastro"
        st.rerun()

def tela_cadastro():
    mostrar_titulo_com_shrek("Cadastro do SHREK")
    novo_user = st.text_input("Novo usuário")
    nova_senha = st.text_input("Nova senha", type="password")

    if st.button("Cadastrar"):
        df = pd.read_csv(ARQ_USUARIOS)
        df["usuario"] = df["usuario"].astype(str).str.strip()
        df["senha"] = df["senha"].astype(str).str.strip()
        if novo_user.strip() in df["usuario"].values:
            st.warning("Usuário já existe!")
        else:
            novo = pd.DataFrame([{"usuario": novo_user.strip(), "senha": nova_senha.strip()}])
            df = pd.concat([df, novo], ignore_index=True)
            df.to_csv(ARQ_USUARIOS, index=False)
            st.success("Usuário cadastrado!")

    if st.button("Voltar para Login"):
        st.session_state.tela = "login"
        st.rerun()

def painel():
    mostrar_titulo_com_shrek("Lava Rápido do SHREK")
    if st.button("Sair"):
        st.session_state.logado = False
        st.session_state.tela = "login"
        st.rerun()

    st.subheader("Nova Lavagem")
    funcionario = st.text_input("Funcionário")
    tipo = st.selectbox("Tipo de Lavagem", ["Simples", "Completa"])
    data = st.date_input("Data")
    hora = st.time_input("Hora")
    pagamento = st.selectbox("Forma de Pagamento", ["Dinheiro", "Cartão", "Pix"])

    if st.button("Salvar"):
        if funcionario.strip() == "":
            st.warning("Digite o nome do funcionário!")
        else:
            dia = data.strftime("%A")
            novo = pd.DataFrame([{
                "Funcionario": funcionario.strip(),
                "Tipo Lavagem": tipo,
                "Data": data,
                "Dia": dia,
                "Hora": hora,
                "Pagamento": pagamento
            }])
            df = pd.read_csv(ARQ_LAVAGENS)
            df = pd.concat([df, novo], ignore_index=True)
            df.to_csv(ARQ_LAVAGENS, index=False)
            st.success("Lavagem registrada com sucesso!")

    st.subheader("Registros do Dia")
    df = pd.read_csv(ARQ_LAVAGENS)
    st.dataframe(df)

# ---------------- CONTROLE DE TELA ----------------
if not st.session_state.logado:
    if st.session_state.tela == "login":
        tela_login()
    elif st.session_state.tela == "cadastro":
        tela_cadastro()
else:
    painel()