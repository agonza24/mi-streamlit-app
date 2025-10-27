import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Dashboard de Ventas", layout="wide")

st.title("📊 Dashboard de Ventas")
st.write("Sube un archivo CSV con tus datos y analiza fácilmente.")

# 1️⃣ Subida del CSV
uploaded_file = st.file_uploader("📂 Sube tu archivo CSV", type=["csv"])

if uploaded_file is not None:
    # Leer datos
    df = pd.read_csv(uploaded_file)

    st.subheader("Vista previa de los datos")
    st.dataframe(df.head())

    # 2️⃣ Seleccionar columna para filtrar
    columnas = df.columns.tolist()
    with st.sidebar:
        st.header("⚙️ Filtros")
        columna_filtro = st.selectbox("Selecciona columna para filtrar:", columnas)
        valores_unicos = df[columna_filtro].dropna().unique().tolist()
        valores_seleccionados = st.multiselect("Selecciona uno o más valores:", valores_unicos)

    # Aplicar filtro si hay selección
    if valores_seleccionados:
        df_filtrado = df[df[columna_filtro].isin(valores_seleccionados)]
        st.write(f"Mostrando {len(df_filtrado)} registros filtrados.")
    else:
        df_filtrado = df
        st.write(f"Mostrando todos los {len(df)} registros.")

    # 3️⃣ Selección de columnas numéricas para graficar
    columnas_numericas = df_filtrado.select_dtypes(include=["number"]).columns.tolist()
    if columnas_numericas:
        col_x = st.selectbox("Eje X:", columnas)
        col_y = st.selectbox("Eje Y (numérico):", columnas_numericas)

        # 4️⃣ Generar gráfico
        st.subheader("📈 Gráfico")
        fig, ax = plt.subplots()
        ax.bar(df_filtrado[col_x], df_filtrado[col_y])
        plt.xticks(rotation=45)
        st.pyplot(fig)
    else:
        st.warning("No se encontraron columnas numéricas para graficar.")
else:
    st.info("👆 Sube un archivo CSV para comenzar.")
