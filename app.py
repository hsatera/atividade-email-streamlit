import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Carregar dados
df = pd.read_csv('dicionario.csv')
dominio_data = {
   "Pesquisa Médica, Gestão em Saúde, Comunicação e Docência": {
    "Fácil": [
      1,
      2,
      15,
      18,
      23
    ],
    "Intermediária": [
      16
    ]
  },
  "Abordagem Familiar": {
    "Intermediária": [
      3
    ]
  },
  "Vigilância em Saúde": {
    "Fácil": [
      4,
      21
    ],
    "Intermediária": [
      5,
      20
    ]
  },
  "Abordagem Individual": {
    "Fácil": [
      6,
      7,
      8,
      9,
      19,
      21,
      22,
      23,
      24,
      26,
      27,
      28,
      29,
      30,
      34,
      37,
      39
    ],
    "Intermediária": [
      10,
      16
    ]
  },
  "Atenção à Saúde": {
    "Fácil": [
      6,
      7,
      8,
      9,
      13,
      15,
      18,
      19,
      26,
      27,
      28,
      29,
      30,
      35,
      37,
      39
    ],
    "Intermediária": [
      16,
      20
    ]
  },
  "Gestão e Organização do Processo de Trabalho": {
    "Fácil": [
      6,
      7,
      14,
      23,
      28,
      31,
      36
    ]
  },
  "Raciocínio Clínico": {
    "Fácil": [
      11,
      12,
      15,
      23,
      24,
      29,
      35,
      39
    ],
    "Intermediária": [
      16
    ]
  },
  "Princípios da APS": {
    "Fácil": [
      14,
      23,
      24,
      25,
      31,
      40
    ]
  },
  "Saúde Coletiva": {
    "Fácil": [
      17,
      18,
      19,
      21,
      28,
      31,
      38
    ],
    "Intermediária": [
      20
    ]
  },
  "Trabalho em Equipe Multidisciplinar": {
    "Fácil": [
      28,
      31,
      38
    ]
  },
  "Abordagem Comunitária": {
    "Fácil": [
      32,
      38
    ]
  },
  "Avaliação da Qualidade e Auditoria": {
    "Fácil": [
      33,
      36
    ]
  }
}
}

# Configurar página
st.title('📝 Sistema de Correção de Provas')
st.subheader('Preencha suas informações:')

with st.form(key='user_info'):
    # Seção de informações do usuário
    col1, col2 = st.columns(2)
    with col1:
        usuario = st.selectbox('Categoria:', ['R1', 'R2'])
    with col2:
        programa = st.selectbox('Programa:', ['Unicamp', 'PMC-CHOV', 'PMC-GATTI', 'PUCCAMP'])
    
    # Seção de respostas
    st.subheader('Marque suas respostas:')
    respostas_usuario = {}
    cols = st.columns(4)
    for i in range(40):
        with cols[i % 4]:
            respostas_usuario[i+1] = st.selectbox(
                f'Questão {i+1}',
                ['A', 'B', 'C', 'D'],
                key=f'q{i+1}'
            )
    
    submitted = st.form_submit_button('Submeter Respostas')

if submitted:
    # Cálculo de resultados
    acertos_total = 0
    acertos_dominio = {dominio: {'Fácil':0, 'Intermediária':0} for dominio in dominio_data}
    acertos_dificuldade = {'Fácil':0, 'Intermediária':0}
    total_por_dificuldade = {'Fácil':0, 'Intermediária':0}

    # Processar cada domínio e dificuldade
    for dominio, dificuldades in dominio_data.items():
        for dificuldade, questoes in dificuldades.items():
            total_por_dificuldade[dificuldade] += len(questoes)
            
            for q in questoes:
                if respostas_usuario[q] == df.at[q-1, 'GABARITO']:
                    acertos_dominio[dominio][dificuldade] += 1
                    acertos_dificuldade[dificuldade] += 1
                    acertos_total += 1

    # Seção de resultados individuais
    st.subheader('📋 Correção Questão a Questão')
    for i in range(40):
        q = i + 1
        resposta = respostas_usuario[q]
        gabarito = df.at[i, 'GABARITO']
        cor = 'green' if resposta == gabarito else 'red'
        
        st.markdown(f"""
        <div style="padding:10px; margin:5px; border-radius:5px; background-color:{cor}20;">
            Questão {q}: <strong style="color:{cor}">{resposta}</strong> | 
            Gabarito: {gabarito}
        </div>
        """, unsafe_allow_html=True)

    # Métricas gerais
    st.subheader('📊 Desempenho Geral')
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total de Acertos", f"{acertos_total}/40")
    with col2:
        st.metric("Percentual de Acertos", f"{(acertos_total/40*100):.1f}%")
    with col3:
        st.metric("Programa", programa)

    # Gráfico de domínios
    st.subheader('📈 Desempenho por Domínio')
    fig, ax = plt.subplots(figsize=(10,8))
    dominios = [d.split(',')[0][:20]+'...' if len(d) > 20 else d for d in dominio_data.keys()]
    valores = [sum(acertos.values()) for acertos in acertos_dominio.values()]
    
    ax.barh(dominios, valores, color='#3498db')
    ax.set_xlabel('Número de Acertos')
    plt.xticks(range(0, max(valores)+2))
    plt.tight_layout()
    st.pyplot(fig)

    # Gráfico de dificuldade
    st.subheader('📉 Acertos por Nível de Dificuldade')
    fig2, ax2 = plt.subplots()
    dificuldades = ['Fácil', 'Intermediária']
    width = 0.35
    
    ax2.bar(dificuldades, total_por_dificuldade.values(), width, label='Total', color='#e74c3c')
    ax2.bar(dificuldades, acertos_dificuldade.values(), width, label='Acertos', color='#2ecc71')
    
    ax2.set_ylabel('Número de Questões')
    ax2.legend()
    st.pyplot(fig2)

    # Informações do candidato
    st.subheader('👤 Dados do Candidato')
    st.write(f"""
    - Categoria: {usuario}
    - Programa: {programa}
    - Data/Hora da Submissão: {pd.Timestamp.now().strftime('%d/%m/%Y %H:%M')}
    """)
