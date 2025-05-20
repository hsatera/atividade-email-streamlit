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
    "Abordagem Familiar e Comunitária": {
        "Intermediária": [3, 32, 38]
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
        "Fácil": [14, 23, 24, 25, 28, 31, 38, 40]
    },
    "Saúde Coletiva": {
        "Fácil": [17, 18, 19, 21, 28, 31, 33, 36, 38],
        "Intermediária": [20]
    }
}

# Configurar página
st.title('📝 Avaliação PMMC I 2025')
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
        erros_dominio = {dominio: 0 for dominio in dominio_data} # Adicionado contador de erros
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
                    else:
                        erros_dominio[dominio] += 1 # Incrementa o contador de erros para o domínio

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

        # Se você quiser uma linha divisória aqui, use:
        st.markdown("---") 

        # Gráfico de Desempenho por Domínio (Acertos e Erros)
        st.subheader('📈 Desempenho por Domínio')
        
        # Pega os nomes completos dos domínios
        dominios_nomes = list(dominio_data.keys()) 
        # Inverte a ordem para que o primeiro domínio apareça no topo do gráfico
        dominios_nomes.reverse() 
        
        # Pega os valores de acertos e erros na ordem invertida dos domínios
        acertos = [acertos_dominio[d] for d in dominios_nomes]
        erros = [erros_dominio[d] for d in dominios_nomes]

        # Ajusta o tamanho da figura dinamicamente para acomodar nomes longos
        # e o número de domínios. Um fator de 0.65 tende a funcionar bem.
        fig, ax = plt.subplots(figsize=(12, len(dominios_nomes) * 0.65)) 

        # Plota as barras de acertos (verde)
        bars_acertos = ax.barh(dominios_nomes, acertos, color='#27ae60', label='Acertos') # Verde
        
        # Plota as barras de erros (vermelho), empilhadas sobre as de acertos
        bars_erros = ax.barh(dominios_nomes, erros, left=acertos, color='#e74c3c', label='Erros') # Vermelho

        ax.set_xlabel('Número de Questões')
        ax.set_title('Acertos e Erros por Domínio')
        ax.legend(loc='lower right') # Adiciona a legenda em uma posição que não atrapalhe os nomes

        # Adiciona os rótulos de valores dentro das barras
        for i, (a, e) in enumerate(zip(acertos, erros)):
            # Rótulo para acertos
            if a > 0: # Mostra o rótulo apenas se houver acertos
                ax.text(a / 2, i, str(a), ha='center', va='center', color='white', fontweight='bold', fontsize=9)
            
            # Rótulo para erros
            if e > 0: # Mostra o rótulo apenas se houver erros
                ax.text(a + e / 2, i, str(e), ha='center', va='center', color='white', fontweight='bold', fontsize=9)
            
            # Opcional: Rótulo do total de questões por domínio (pode poluir)
            # total_questoes_dominio = a + e
            # ax.text(total_questoes_dominio + 0.5, i, f'({total_questoes_dominio})', ha='left', va='center', color='black', fontsize=8)


        plt.tight_layout() # Ajusta o layout para evitar sobreposições
        st.pyplot(fig) # Exibe o gráfico no Streamlit
