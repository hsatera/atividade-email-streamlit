import pandas as pd
import streamlit as st

# Função para buscar atividades por email
def buscar_atividades_por_email(email_usuario, df):
    atividades_usuario = df[df['Endereço de e-mail'] == email_usuario]
    if not atividades_usuario.empty:
        return atividades_usuario[['Carimbo de data/hora', 'TEMA DA ATIVIDADE']]
    else:
        return "Nenhuma atividade encontrada para o email informado."

# Carregar o arquivo CSV
uploaded_file = st.file_uploader("Escolha o arquivo CSV", type="csv")

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    # Input do usuário para o email
    email = st.text_input("Insira seu e-mail:")

    # Botão para buscar atividades
    if st.button('Buscar Atividades'):
        resultado = buscar_atividades_por_email(email, df)
        st.write(resultado)
