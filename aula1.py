import streamlit as st
import pandas as pd
import plotly.express as px

st.write("""
### Integrantes
Julia Armando 
Beatriz Lauton
Ada Mirella
""")


import streamlit as st
import pandas as pd
import plotly.express as px

# --------------------------------------------------
# CONFIGURAÇÃO DA PÁGINA
# --------------------------------------------------

st.set_page_config(
    page_title="Explorador Musical",
    page_icon="♪𝄞♫ᝰ.ᐟ",
    layout="wide"
)

st.title("♪𝄞♫ᝰ.ᐟ Explorador Musical ♪𝄞♫ᝰ")
st.write("Explore características, gêneros e popularidade das músicas do dataset.")


# --------------------------------------------------
# CARREGAR OS DADOS
# --------------------------------------------------

@st.cache_data
def carregar_dados():
    df = pd.read_csv("dataset.csv")

    # Remove coluna desnecessária criada no CSV
    if "Unnamed: 0" in df.columns:
        df = df.drop(columns=["Unnamed: 0"])

    # Converter duração de milissegundos para minutos
    df["duration_min"] = df["duration_ms"] / 60000

    return df


df = carregar_dados()


# --------------------------------------------------
# BARRA LATERAL - FILTROS
# --------------------------------------------------

st.sidebar.header("🎛️ Filtros")

generos = sorted(df["track_genre"].dropna().unique())

generos_selecionados = st.sidebar.multiselect(
    "Escolha os gêneros:",
    generos
)

popularidade_minima = st.sidebar.slider(
    "Popularidade mínima:",
    min_value=0,
    max_value=100,
    value=0
)

explicit_filter = st.sidebar.selectbox(
    "Conteúdo explícito:",
    ["Todos", "Não explícito", "Explícito"]

)

df_filtrado = df.copy()

# Filtro por artista
artista_pesquisado = st.sidebar.text_input(
    "🎤 Pesquisar cantor ou artista:",
    placeholder="Ex: Taylor Swift"
)

if artista_pesquisado:
    df_filtrado = df_filtrado[
        df_filtrado["artists"]
        .str.contains(artista_pesquisado, case=False, na=False)
    ]

# Filtro por gênero
if generos_selecionados:
    df_filtrado = df_filtrado[
        df_filtrado["track_genre"].isin(generos_selecionados)
    ]

# Filtro de popularidade
df_filtrado = df_filtrado[
    df_filtrado["popularity"] >= popularidade_minima
]


# --------------------------------------------------
# APLICAR FILTROS
# --------------------------------------------------

df_filtrado = df.copy()

# FILTRO POR ARTISTA
if artista_pesquisado:
    df_filtrado = df_filtrado[
        df_filtrado["artists"].str.contains(
            artista_pesquisado,
            case=False,
            na=False
        )
    ]

# FILTRO POR GÊNERO
if generos_selecionados:
    df_filtrado = df_filtrado[
        df_filtrado["track_genre"].isin(generos_selecionados)
    ]

# FILTRO POR POPULARIDADE
df_filtrado = df_filtrado[
    df_filtrado["popularity"] >= popularidade_minima
]

# FILTRO POR CONTEÚDO EXPLÍCITO
if explicit_filter == "Explícito":
    df_filtrado = df_filtrado[
        df_filtrado["explicit"] == True
    ]

elif explicit_filter == "Não explícito":
    df_filtrado = df_filtrado[
        df_filtrado["explicit"] == False
    ]

# --------------------------------------------------
# INDICADORES
# --------------------------------------------------

st.subheader("📈 Visão geral")

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "𝄞⨾𓍢ִ໋  Músicas",
    f"{len(df_filtrado):,}"
)

col2.metric(
    "🎤︎︎ Artistas",
    f"{df_filtrado['artists'].nunique():,}"
)

col3.metric(
    "𑣲𝄞 Gêneros",
    df_filtrado["track_genre"].nunique()
)

if not df_filtrado.empty:
    popularidade_media = df_filtrado["popularity"].mean()
else:
    popularidade_media = 0

col4.metric(
    "✯ Popularidade média",
    f"{popularidade_media:.1f}"
)


st.divider()


# --------------------------------------------------
# GÊNEROS MAIS POPULARES
# --------------------------------------------------

st.subheader("✯ Gêneros mais populares ✯")

popularidade_genero = (
    df_filtrado
    .groupby("track_genre", as_index=False)["popularity"]
    .mean()
    .sort_values("popularity", ascending=False)
    .head(15)
)

fig_generos = px.bar(
    popularidade_genero,
    x="track_genre",
    y="popularity",
    labels={
        "track_genre": "Gênero",
        "popularity": "Popularidade média"
    },
    title="Top 15 gêneros por popularidade média"
)

st.plotly_chart(fig_generos, use_container_width=True)


# --------------------------------------------------
# ENERGIA X POPULARIDADE
# --------------------------------------------------

st.subheader("๋࣭ ⚡︎⭑ Energia x Popularidade ๋࣭ ⚡︎⭑")

# Amostra para evitar deixar o gráfico pesado
if len(df_filtrado) > 5000:
    df_scatter = df_filtrado.sample(5000, random_state=42)
else:
    df_scatter = df_filtrado

fig_energia = px.scatter(
    df_scatter,
    x="energy",
    y="popularity",
    color="track_genre",
    hover_data=[
        "track_name",
        "artists"
    ],
    labels={
        "energy": "Energia",
        "popularity": "Popularidade",
        "track_genre": "Gênero"
    }
)

st.plotly_chart(fig_energia, use_container_width=True)


# --------------------------------------------------
# DANÇABILIDADE X POPULARIDADE
# --------------------------------------------------

st.subheader("𓀤 Dançabilidade x Popularidade 𓀥")

fig_danca = px.scatter(
    df_scatter,
    x="danceability",
    y="popularity",
    color="track_genre",
    hover_data=[
        "track_name",
        "artists"
    ],
    labels={
        "danceability": "Dançabilidade",
        "popularity": "Popularidade",
        "track_genre": "Gênero"
    }
)

st.plotly_chart(fig_danca, use_container_width=True)


# --------------------------------------------------
# VALÊNCIA
# --------------------------------------------------

st.subheader("☺︎ Positividade dos gêneros ☺︎")

valencia_genero = (
    df_filtrado
    .groupby("track_genre", as_index=False)["valence"]
    .mean()
    .sort_values("valence", ascending=False)
    .head(15)
)

fig_valencia = px.bar(
    valencia_genero,
    x="track_genre",
    y="valence",
    labels={
        "track_genre": "Gênero",
        "valence": "Valência média"
    },
    title="Gêneros com maior valência média"
)

st.plotly_chart(fig_valencia, use_container_width=True)


# --------------------------------------------------
# DURAÇÃO DAS MÚSICAS
# --------------------------------------------------

st.subheader("⏱ Duração das músicas ⏱")

fig_duracao = px.histogram(
    df_filtrado,
    x="duration_min",
    nbins=50,
    labels={
        "duration_min": "Duração (minutos)"
    },
    title="Distribuição da duração das músicas"
)

st.plotly_chart(fig_duracao, use_container_width=True)


# --------------------------------------------------
# TOP MÚSICAS
# --------------------------------------------------

st.subheader("🎖 Músicas mais populares 🎖")

top_musicas = (
    df_filtrado[
        [
            "track_name",
            "artists",
            "track_genre",
            "popularity",
            "energy",
            "danceability",
            "valence"
        ]
    ]
    .sort_values("popularity", ascending=False)
    .head(20)
)

st.dataframe(
    top_musicas,
    use_container_width=True,
    hide_index=True
)


# --------------------------------------------------
# DADOS DO DATASET
# --------------------------------------------------

with st.expander("˖⌕ ۫  Ver dados utilizados ˖⌕ ۫ "):
    st.dataframe(
        df_filtrado,
        use_container_width=True
    )

