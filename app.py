import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Dados do gabarito
gabarito_data = {
    1: 'B', 2: 'C', 3: 'D', 4: 'C', 5: 'B', 6: 'D', 7: 'B', 8: 'D', 9: 'B', 10: 'C',
    11: 'A', 12: 'D', 13: 'C', 14: 'A', 15: 'A', 16: 'C', 17: 'A', 18: 'A', 19: 'C', 20: 'C',
    21: 'A', 22: 'B', 23: 'A', 24: 'C', 25: 'D', 26: 'C', 27: 'C', 28: 'B', 29: 'C', 30: 'D',
    31: 'C', 32: 'C', 33: 'A', 34: 'C', 35: 'D', 36: 'A', 37: 'B', 38: 'B', 39: 'C', 40: 'C'
}

# Criar DataFrame com o gabarito
df = pd.DataFrame(list(gabarito_data.items()), columns=['QUESTAO', 'GABARITO'])
df.set_index('QUESTAO', inplace=True)

# Dicionário de domínios e questões
dominio_data = {
    "Pesquisa Médica, Gestão em Saúde, Comunicação e Docência": {
        "Fácil": [1, 2, 15, 18, 23],
        "Intermediária": [16]
    },
    "Abordagem Familiar": {
        "Intermediária": [3]
    },
    "Vigilância em Saúde": {
        "Fácil": [4, 21],
        "Intermediária": [5, 20]
    },
    "Abordagem Individual": {
        "Fácil": [6, 7, 8, 9, 19, 21, 22, 23, 24, 26, 27, 28, 29, 30, 34, 37, 39],
        "Intermediária": [10, 16]
    },
    "Atenção à Saúde": {
        "Fácil": [6, 7, 8, 9, 13, 15, 18, 19, 26, 27, 28, 29, 30, 35, 37, 39],
        "Intermediária": [16, 20]
    },
    "Gestão e Organização do Processo de Trabalho": {
        "Fácil": [6, 7, 14, 23, 28, 31, 36]
    },
    "Raciocínio Clínico": {
        "Fácil": [11, 12, 15, 23, 24, 29, 35, 39],
        "Intermediária": [16]
    },
    "Princípios da APS": {
        "Fácil": [14, 23, 24, 25, 31, 40]
    },
    "Saúde Coletiva": {
        "Fácil": [17, 18, 19, 21, 28, 31, 38],
        "Intermediária": [20]
    },
    "Trabalho em Equipe Multidisciplinar": {
        "Fácil": [28, 31, 38]
    },
    "Abordagem Comunitária": {
        "Fácil": [32, 38]
    },
    "Avaliação da Qualidade e Auditoria": {
        "Fácil": [33, 36]
    }
}

# Configurar página
st.title('📝 Correção Avaliação PMMC I 2025')
st.subheader('Marque suas respostas:')

with st.form(key='user_answers'):
    respostas_usuario = {}
    cols = st.columns(4)
    for i in range(40):
        with cols[i % 4]:
            respostas_usuario[i+1] = st.selectbox(
                f'Questão {i+1}',
                ['', 'A', 'B', 'C', 'D'],  # começa vazia, obrigando a escolher
                key=f'q{i+1}'
            )
    submitted = st.form_submit_button('Submeter Respostas')

if submitted:
    # Verifica se todas as questões foram respondidas
    nao_respondidas = [q for q, r in respostas_usuario.items() if r == '']
    if nao_respondidas:
        st.error(f"⚠️ Você precisa responder todas as questões antes de submeter. Questões faltando: {', '.join(map(str, nao_respondidas))}")
    else:
        acertos_total = 0
        acertos_dominio = {dominio: 0 for dominio in dominio_data}
        total_por_dominio = {dominio: 0 for dominio in dominio_data}

        for questao, resposta_usuario_atual in respostas_usuario.items():
            gabarito_correto = df.loc[questao, 'GABARITO']
            if resposta_usuario_atual == gabarito_correto:
                acertos_total += 1

        for dominio, dificuldades in dominio_data.items():
            for dificuldade, questoes in dificuldades.items():
                total_por_dominio[dominio] += len(questoes)
                for q in questoes:
                    resposta = respostas_usuario.get(q, '')
                    if resposta == df.loc[q, 'GABARITO']:
                        acertos_dominio[dominio] += 1

        # Calcular porcentagem de acertos por domínio
        porcentagem_acertos_dominio = {}
        for dominio, acertos in acertos_dominio.items():
            total = total_por_dominio[dominio]
            porcentagem_acertos_dominio[dominio] = (acertos / total * 100) if total > 0 else 0

        # Gabarito com feedback
        st.subheader('🔑 Gabarito da Prova')
        cols_gabarito = st.columns(5)
        for i in range(40):
            questao = i + 1
            resposta_user = respostas_usuario.get(questao, '')
            gabarito_correto = df.loc[questao, 'GABARITO']
            texto = f'**{questao}:** '
            if resposta_user == gabarito_correto:
                texto += f'<span style="background-color:#90EE90">{gabarito_correto}</span>'
            else:
                texto += f'<span style="text-decoration: line-through; color:red;">{resposta_user}</span> <span style="color:green;">{gabarito_correto}</span>'

            with cols_gabarito[i % 5]:
                st.markdown(texto, unsafe_allow_html=True)

        # Boletim final
        st.subheader('📊 Boletim Final')
        col_nota, col_perc_total = st.columns(2)
        with col_nota:
            st.metric("Nota Final (Acertos)", f"{acertos_total}/40")
        with col_perc_total:
            st.metric("Percentual Total de Acertos", f"{(acertos_total / 40 * 100):.1f}%")

        # Gráfico desempenho por domínio
        st.subheader('📈 Desempenho por Domínio')
        fig, ax = plt.subplots(figsize=(10, 8))
        dominios = [d.split(',')[0][:20] + '...' if len(d) > 20 else d for d in dominio_data.keys()]
        porcentagens = list(porcentagem_acertos_dominio.values())

        bars = ax.barh(dominios, porcentagens, color='#27ae60')
        ax.set_xlabel('Percentual de Acertos (%)')
        ax.set_xlim(0, 100)
        ax.invert_yaxis()

        for bar, perc in zip(bars, porcentagens):
            width = bar.get_width()
            ax.text(width + 1, bar.get_y() + bar.get_height() / 2, f'{perc:.1f}%', ha='left', va='center')

        plt.tight_layout()
        st.pyplot(fig)
