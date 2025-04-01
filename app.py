import streamlit as st
import math
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

st.set_page_config(page_title="Calculadora Interés Compuesto", layout="centered")
st.title("Calculadora de Interés Compuesto")

# ---------- SELECCIÓN DE PREGUNTA ----------
pregunta = st.selectbox(
    "¿Qué deseas calcular?",
    [
        "¿Cuánto puedo ahorrar?",
        "¿Cuánto tardaré en alcanzar mi objetivo de ahorro?",
        "¿Cuánto necesito ahorrar en cada período para lograr mi objetivo de ahorro?",
        "¿Qué porcentaje de interés necesito para llegar a mi objetivo de ahorro?"
    ]
)

# ---------- FRECUENCIA Y MOMENTO DEL DEPÓSITO ----------
st.sidebar.header("Parámetros comunes")
frecuencia = st.sidebar.selectbox("Frecuencia de depósito", ["Semanalmente", "Bi-semanalmente", "Mensualmente", "Anualmente"])
m = {"Semanalmente": 52, "Bi-semanalmente": 26, "Mensualmente": 12, "Anualmente": 1}[frecuencia]
momento = st.sidebar.selectbox("Momento del depósito", ["Inicio del período", "Final del período"])

# ---------- OPCIÓN 1: ¿CUÁNTO PUEDO AHORRAR? ----------
if pregunta == "¿Cuánto puedo ahorrar?":
    st.subheader("¿Cuánto puedo ahorrar?")
    inicial = st.number_input("Balance inicial (€)", value=1000.0)
    deposito = st.number_input("Depósito periódico (€)", value=100.0)
    interes_anual = st.number_input("Ratio de interés anual (%)", value=8.0)
    años = st.number_input("Duración (años)", value=10)

    r = interes_anual / 100 / m
    n = int(años * m)
    saldo = inicial
    historial = []

    for periodo in range(1, n + 1):
        if momento == "Inicio del período":
            saldo += deposito
        saldo *= (1 + r)
        if momento == "Final del período":
            saldo += deposito
        if periodo % m == 0:
            historial.append({
                "Año": periodo // m,
                "Depósito anual": deposito * m,
                "Depósitos totales": deposito * periodo,
                "Interés acumulado": saldo - inicial - deposito * periodo,
                "Balance": saldo
            })

    df = pd.DataFrame(historial)

    st.markdown(f"### Puedes ahorrar **{saldo:,.2f} €** en {años:.0f} años")
    st.markdown(f"Aportando {deposito:.2f} € {frecuencia.lower()}, con un {interes_anual}% anual")

    col1, col2, col3 = st.columns(3)
    col1.metric("Balance inicial", f"{inicial:,.2f} €")
    col2.metric("Depósitos totales", f"{deposito * n:,.2f} €")
    col3.metric("Interés ganado", f"{saldo - inicial - deposito * n:,.2f} €")

    # ---------- GRÁFICO ----------
    st.subheader("Evolución del capital")
    fig, ax = plt.subplots()
    ax.bar(df["Año"], inicial, label="Inicial")
    ax.bar(df["Año"], df["Depósitos totales"], bottom=inicial, label="Depósitos")
    ax.bar(df["Año"], df["Interés acumulado"], bottom=inicial + df["Depósitos totales"], label="Interés")
    ax.set_xlabel("Años")
    ax.set_ylabel("€")
    ax.set_title("Ahorro acumulado")
    ax.legend()
    st.pyplot(fig)

    # ---------- TABLA ----------
    st.subheader("Detalle año a año")
    st.dataframe(df.style.format({
        "Depósito anual": "€{:,.2f}",
        "Depósitos totales": "€{:,.2f}",
        "Interés acumulado": "€{:,.2f}",
        "Balance": "€{:,.2f}"
    }))

# ---------- OPCIÓN 2: ¿CUÁNTO TARDARÉ EN ALCANZAR MI OBJETIVO? ----------
elif pregunta == "¿Cuánto tardaré en alcanzar mi objetivo de ahorro?":
    st.subheader("¿Cuánto tardaré en alcanzar mi objetivo de ahorro?")

    objetivo = st.number_input("Objetivo de ahorro (€)", value=10000.0)
    inicial = st.number_input("Balance inicial (€)", value=1000.0)
    deposito = st.number_input("Depósito periódico (€)", value=100.0)
    interes_anual = st.number_input("Ratio de interés anual (%)", value=8.0)

    r = interes_anual / 100 / m
    saldo = inicial
    historial = []
    periodo = 0

    while saldo < objetivo and periodo < 1000:
        if momento == "Inicio del período":
            saldo += deposito
        saldo *= (1 + r)
        if momento == "Final del período":
            saldo += deposito

        periodo += 1
        if periodo % m == 0:
            historial.append({
                "Año": periodo // m,
                "Depósito acumulado": deposito * periodo,
                "Interés acumulado": saldo - inicial - deposito * periodo,
                "Balance": saldo
            })

    if saldo >= objetivo:
        años_necesarios = periodo / m
        st.markdown(f"### Necesitarás **{periodo} períodos** ({años_necesarios:.2f} años) para alcanzar {objetivo:,.2f} €")
        st.markdown(f"Con aportes de {deposito:.2f} € cada {frecuencia.lower()} y un {interes_anual}% de interés anual")

        df = pd.DataFrame(historial)

        col1, col2, col3 = st.columns(3)
        col1.metric("Depósitos totales", f"{deposito * periodo:,.2f} €")
        col2.metric("Interés ganado", f"{saldo - inicial - deposito * periodo:,.2f} €")
        col3.metric("Balance final", f"{saldo:,.2f} €")

        # ---------- GRÁFICO ----------
        st.subheader("Evolución del capital")
        fig, ax = plt.subplots()
        ax.plot(df["Año"], df["Balance"], label="Balance acumulado", marker='o')
        ax.axhline(y=objetivo, color='r', linestyle='--', label="Objetivo")
        ax.set_xlabel("Años")
        ax.set_ylabel("€")
        ax.set_title("Crecimiento del ahorro hasta alcanzar el objetivo")
        ax.legend()
        st.pyplot(fig)

        # ---------- TABLA ----------
        st.subheader("Detalle año a año")
        st.dataframe(df.style.format({
            "Depósito acumulado": "€{:,.2f}",
            "Interés acumulado": "€{:,.2f}",
            "Balance": "€{:,.2f}"
        }))
    else:
        st.error("No se alcanzó el objetivo en un plazo razonable (más de 1000 períodos). Revisa los parámetros.")
# ---------- LAS OTRAS OPCIONES (solo texto de momento, luego se mejora) ----------

elif pregunta == "¿Cuánto necesito ahorrar en cada período para lograr mi objetivo de ahorro?":
    st.info("👉 Próximamente añadiremos la visualización para esta opción.")
elif pregunta == "¿Qué porcentaje de interés necesito para llegar a mi objetivo de ahorro?":
    st.info("👉 También lo haremos visual 😉")

