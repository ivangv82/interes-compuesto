import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Título de la aplicación
st.title("Calculadora de Interés Compuesto")

# Sección lateral para ingresar los parámetros de la inversión
st.sidebar.header("Parámetros de la inversión")
inversion_inicial = st.sidebar.number_input("Inversión Inicial ($)", value=1000, step=100)
aporte_mensual = st.sidebar.number_input("Aporte Mensual ($)", value=100, step=50)
tasa_interes_anual = st.sidebar.number_input("Tasa de Interés Anual (%)", value=5.0, step=0.1)
periodo_inversion = st.sidebar.number_input("Número de Años", value=10, step=1)

# Conversión de la tasa anual a tasa mensual
tasa_mensual = (tasa_interes_anual / 100) / 12
numero_periodos = int(periodo_inversion * 12)

# Inicializamos la lista para guardar el balance de cada mes
meses = []
balances = []
balance_actual = inversion_inicial

# Calculamos el balance mes a mes
for mes in range(1, numero_periodos + 1):
    balance_actual = balance_actual * (1 + tasa_mensual) + aporte_mensual
    meses.append(mes)
    balances.append(balance_actual)

# Creamos un DataFrame con los resultados
df = pd.DataFrame({
    "Mes": meses,
    "Balance ($)": balances
})

# Mostramos el balance final
st.subheader("Balance Final")
st.write(f"Después de {numero_periodos} meses, el balance será de aproximadamente: **${balance_actual:,.2f}**")

# Graficamos la curva de inversión
st.subheader("Evolución de la Inversión")
fig, ax = plt.subplots()
ax.plot(df["Mes"], df["Balance ($)"], marker="o", linewidth=2)
ax.set_xlabel("Mes")
ax.set_ylabel("Balance ($)")
ax.set_title("Curva de Crecimiento de la Inversión")
st.pyplot(fig)

# Mostramos la tabla de datos
st.subheader("Detalle Mensual")
st.dataframe(df)

