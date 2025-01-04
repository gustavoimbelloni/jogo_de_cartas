import random
import streamlit as st

# Funções do jogo de cartas
def gerar_baralho(n_copias=2, coringas=True, embaralhado=True):
    baralho = []
    naipes = list('♠♣♥♦')
    numeros = list('A23456789') + ['10'] + list('JQK')

    for _ in range(n_copias):
        for naipe in naipes:
            for numero in numeros:
                carta = numero + naipe
                baralho.append(carta)
        if coringas:
            baralho.extend(['JK1', 'JK2'])
    if embaralhado:
        random.shuffle(baralho)
    return baralho

def dar_as_cartas(baralho, n_jogadores=4, n_cartas=5):
    jogadores = {}
    for i in range(n_jogadores):
        mao = []
        while len(mao) < n_cartas:
            if not baralho:
                st.warning("O baralho acabou antes de distribuir todas as cartas!")
                break
            carta = baralho.pop(0)
            mao.append(carta)
        nome_jogador = f'Jogador {i+1}'
        jogadores[nome_jogador] = mao
    return jogadores

# Configuração do Streamlit
st.title("Jogo de Cartas 🎴")
st.sidebar.header("Configurações do Baralho")

# Entrada do usuário
n_copias = st.sidebar.number_input("Número de cópias do baralho", min_value=1, max_value=5, value=2, step=1)
coringas = st.sidebar.checkbox("Incluir coringas", value=True)
embaralhado = st.sidebar.checkbox("Embaralhar o baralho", value=True)
n_jogadores = st.sidebar.number_input("Número de jogadores", min_value=1, max_value=10, value=4, step=1)
n_cartas = st.sidebar.number_input("Cartas por jogador", min_value=1, max_value=10, value=5, step=1)

# Gerar baralho
if st.sidebar.button("Gerar Baralho"):
    baralho = gerar_baralho(n_copias=n_copias, coringas=coringas, embaralhado=embaralhado)
    st.session_state['baralho'] = baralho
    st.success("Baralho gerado com sucesso!")

# Mostrar baralho
if 'baralho' in st.session_state:
    baralho = st.session_state['baralho']
    st.subheader("Baralho Atual")
    st.write(f"Total de cartas no baralho: {len(baralho)}")
    st.text(", ".join(baralho))

    # Distribuir cartas
    if st.button("Distribuir Cartas"):
        jogadores = dar_as_cartas(baralho, n_jogadores=n_jogadores, n_cartas=n_cartas)
        st.session_state['jogadores'] = jogadores
        st.session_state['baralho'] = baralho
        st.success("Cartas distribuídas!")

    # Mostrar jogadores e suas cartas
    if 'jogadores' in st.session_state:
        jogadores = st.session_state['jogadores']
        st.subheader("Jogadores e suas Cartas")
        for jogador, mao in jogadores.items():
            st.write(f"**{jogador}:** {', '.join(mao)}")

    # Mostrar baralho restante
    st.subheader("Cartas Restantes no Baralho")
    st.write(f"Total de cartas restantes: {len(baralho)}")
    st.text(", ".join(baralho))
