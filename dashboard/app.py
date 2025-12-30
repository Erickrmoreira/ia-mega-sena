import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="Mega-Sena IA Dashboard",
    layout="wide"
)

st.title("🎯 Mega-Sena Intelligent Generator")

uploaded = st.file_uploader(
    "Upload do CSV de jogos gerados",
    type=["csv"]
)

if uploaded:
    df = pd.read_csv(uploaded)

    st.subheader("📊 Visão Geral")
    st.metric("Total de jogos", len(df))
    st.metric("Score médio", round(df["predicted_score"].mean(), 2))

    st.subheader("🏆 Top 10 Jogos")
    st.dataframe(df.head(10))

    st.subheader("📈 Distribuição de Scores")
    fig, ax = plt.subplots()
    ax.hist(df["predicted_score"], bins=20)
    st.pyplot(fig)

    st.subheader("🔍 Importância das Features")
    feature_cols = [
        c for c in df.columns
        if c not in ["game", "predicted_score"]
    ]

    importance = df[feature_cols].mean()
    st.bar_chart(importance)
