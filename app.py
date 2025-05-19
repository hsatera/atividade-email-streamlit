import streamlit as st
import pandas as pd

# Carregar o gabarito
df = pd.read_csv('dicionario.csv')

# Configurar página
st.title('Verificador de Gabarito')
st.subheader('Marque suas respostas:')

# Criar inputs para todas as questões
respostas_usuario = {}
cols = st.columns(4)

for i, row in df.iterrows():
    with cols[i % 4]:
        respostas_usuario[i+1] = st.selectbox(
            f'Questão {i+1}',
            ['A', 'B', 'C', 'D'],
            key=f'q{i+1}'
        )

# Botão para verificar
if st.button('Verificar Respostas'):
    st.subheader('Resultado:')
    
    # Comparar respostas
    for i, row in df.iterrows():
        questao = i + 1
        resposta_correta = row['GABARITO']
        resposta_usuario = respostas_usuario[questao]
        
        # Determinar cor
        cor = 'green' if resposta_usuario == resposta_correta else 'red'
        
        # Exibir resultado
        st.markdown(
            f"""
            <div style="padding: 10px; border-radius: 5px; margin: 5px 0; background-color: {cor}20;">
                🡲 Questão {questao}: 
                <span style="color: {cor}; font-weight: bold;">{resposta_usuario}</span> | 
                Gabarito: {resposta_correta}
            </div>
            """,
            unsafe_allow_html=True
        )
