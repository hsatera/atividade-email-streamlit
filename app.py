import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from collections import defaultdict

# Gabarito oficial (extraído da imagem)
gabarito = [
    "B", "C", "D", "C", "B", "D", "B", "D", "B", "C",
    "A", "D", "C", "A", "A", "C", "A", "A", "C", "C",
    "A", "B", "A", "C", "D", "C", "C", "B", "C", "D",
    "C", "C", "A", "C", "D", "A", "B", "B", "C", "C"
]

# Carregar dados adicionais das questões
df = pd.read_csv("questoes.csv")

def preparar_questoes(df):
    # (Manter a mesma função original para obter domínios e dificuldades)
    return questoes

questoes = preparar_questoes(df)

# Configuração da página
st.set_page_config(page_title="Corretor de Provas", layout="wide")
st.title("📝 Corretor Automático de Provas")

# Inicializar estado da sessão
if 'respostas' not in st.session_state:
    st.session_state.respostas = {}

# Sidebar com instruções
with st.sidebar:
    st.header("Instruções")
    st.markdown("""
    1. Selecione a resposta para cada questão
    2. Clique em **Corrigir Prova** ao final
    3. Veja seu resultado detalhado
    """)

# Formulário de respostas
with st.form(key='prova_form'):
    cols = st.columns(2)
    
    for i in range(40):  # 40 questões fixas
        with cols[0] if i < 20 else cols[1]:
            q_num = i + 1
            options = ["A", "B", "C", "D"]
            resposta = st.radio(
                label=f"Questão {q_num}",
                options=options,
                key=f"q{q_num}",
                horizontal=True
            )
            st.session_state.respostas[q_num] = resposta.upper()
    
    st.form_submit_button("🔍 Corrigir Prova", on_click=lambda: None)

# Processar correção
if st.button("🎯 Mostrar Resultado"):
    acertos = 0
    dominio_stats = defaultdict(lambda: {'total': 0, 'acertos': 0})
    dificuldade_stats = defaultdict(lambda: {'total': 0, 'acertos': 0})
    
    for idx in range(40):
        q_num = idx + 1
        resposta_usuario = st.session_state.respostas.get(q_num, '')
        correta = gabarito[idx]
        
        # Obter dados da questão do CSV
        q_data = next((q for q in questoes if q['numero'] == q_num), {})
        
        # Atualizar estatísticas
        for dominio in q_data.get('dominios', []):
            dominio_stats[dominio]['total'] += 1
            if resposta_usuario == correta:
                dominio_stats[dominio]['acertos'] += 1
                
        dificuldade = q_data.get('dificuldade', 'Não informada')
        dificuldade_stats[dificuldade]['total'] += 1
        if resposta_usuario == correta:
            dificuldade_stats[dificuldade]['acertos'] += 1
            acertos += 1
    
    # Mostrar resultados
    st.success(f"### Pontuação Final: {acertos}/40")
    
    # Gráfico de desempenho por domínio
    if dominio_stats:
        fig, ax = plt.subplots()
        dominios = []
        taxas = []
        for dominio, stats in dominio_stats.items():
            dominios.append(dominio)
            taxas.append((stats['acertos']/stats['total'])*100)
        
        ax.barh(dominios, taxas, color='#4CAF50')
        ax.set_title("Desempenho por Domínio")
        ax.set_xlabel("% de Acertos")
        st.pyplot(fig)
    
    # Gráfico de desempenho por dificuldade
    if dificuldade_stats:
        fig2, ax2 = plt.subplots()
        dificuldades = list(dificuldade_stats.keys())
        taxas = [(dificuldade_stats[d]['acertos']/dificuldade_stats[d]['total'])*100 for d in dificuldades]
        
        ax2.bar(dificuldades, taxas, color='#2196F3')
        ax2.set_title("Desempenho por Dificuldade")
        ax2.set_ylabel("% de Acertos")
        st.pyplot(fig2)
    
    # Tabela detalhada
    detalhes = []
    for idx in range(40):
        q_num = idx + 1
        q_data = next((q for q in questoes if q['numero'] == q_num), {})
        detalhes.append({
            "Questão": q_num,
            "Resposta Correta": gabarito[idx],
            "Sua Resposta": st.session_state.respostas.get(q_num, ''),
            "Domínios": ", ".join(q_data.get('dominios', [])),
            "Dificuldade": q_data.get('dificuldade', 'Não informada'),
            "Acerto": "✅" if st.session_state.respostas.get(q_num, '').upper() == gabarito[idx] else "❌"
        })
    
    st.subheader("📊 Detalhamento por Questão")
    st.dataframe(pd.DataFrame(detalhes), use_container_width=True)

st.markdown("---")
st.caption("Desenvolvido para correção automática de provas - Versão 2.0")
