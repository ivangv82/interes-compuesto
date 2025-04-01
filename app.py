import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

st.title("Calculadora de Interés Compuesto")

# --------------------
# Entradas en la barra lateral
# --------------------
st.sidebar.header("Parámetros de la inversión")
initial_balance = st.sidebar.number_input("Balance inicial (€)", value=1000.00, format="%.2f")
deposit = st.sidebar.number_input("Depósito periódico (€)", value=100.00, format="%.2f")
frequency_option = st.sidebar.selectbox("Frecuencia de depósito", 
    options=["Semanalmente", "Bi-semanalmente", "Mensualmente", "Anualmente"])
timing_option = st.sidebar.selectbox("Momento del depósito", 
    options=["Inicio del período", "Final del período"])
annual_interest = st.sidebar.number_input("Ratio de interés anual (%)", value=1.0, step=0.1)
years = st.sidebar.number_input("Duración (años)", value=10, step=1)

# Mapeo de la frecuencia a número de depósitos por año
if frequency_option == "Semanalmente":
    m = 52
elif frequency_option == "Bi-semanalmente":
    m = 26
elif frequency_option == "Mensualmente":
    m = 12
elif frequency_option == "Anualmente":
    m = 1

r = annual_interest / 100  # convertir porcentaje a decimal

# Botón para ejecutar el cálculo
if st.sidebar.button("Calcular"):
    # Listas para almacenar los resultados año a año
    years_list = []
    fv_list = []              # Valor futuro (balance final) de cada año
    cumulative_deposits_list = []  # Depósitos acumulados (solo los depósitos periódicos)
    interest_list = []        # Interés acumulado de cada año
    
    deposit_yearly = deposit * m  # Depósito total realizado en cada año
    
    # Para cada año se calcula el valor futuro usando la fórmula de interés compuesto
    for i in range(1, int(years) + 1):
        if timing_option == "Final del período":
            FV = initial_balance * (1 + r/m)**(m * i) + deposit * (((1 + r/m)**(m * i) - 1) / (r/m))
        else:  # Depósito al inicio del período
            FV = initial_balance * (1 + r/m)**(m * i) + deposit * (((1 + r/m)**(m * i) - 1) / (r/m)) * (1 + r/m)
        
        principal = initial_balance + deposit_yearly * i  # Suma de la inversión inicial y los depósitos hechos
        interest = FV - principal  # El interés es lo que sobra
        
        years_list.append(i)
        fv_list.append(FV)
        cumulative_deposits_list.append(deposit_yearly * i)
        interest_list.append(interest)
    
    final_FV = fv_list[-1]
    total_deposits = deposit_yearly * years
    total_interest = final_FV - (initial_balance + total_deposits)
    
    # --------------------
    # Resumen principal
    # --------------------
    st.subheader("Resumen principal")
    st.markdown(f"**Puedes ahorrar {final_FV:,.2f} €**")
    st.markdown(f"Ahorro depositando **{deposit:,.2f} €** {frequency_option.lower()} durante **{int(years)}** años")
    
    st.markdown("**Detalles clave:**")
    st.markdown(f"- **Balance inicial:** {initial_balance:,.2f} €")
    st.markdown(f"- **Depósitos totales:** {total_deposits:,.2f} €")
    st.markdown(f"- **Interés total:** {total_interest:,.2f} €")
    
    # --------------------
    # Tabla detallada año a año
    # --------------------
    df = pd.DataFrame({
        "Año": years_list,
        "Depósito Periódico (anual)": [deposit_yearly] * len(years_list),
        "Depósitos Totales": cumulative_deposits_list,
        "Interés": interest_list,
        "Balance": fv_list
    })
    
    st.subheader("Detalle año a año")
    st.dataframe(df.style.format({
        "Depósito Periódico (anual)": "{:,.2f} €",
        "Depósitos Totales": "{:,.2f} €",
        "Interés": "{:,.2f} €",
        "Balance": "{:,.2f} €"
    }))
    
    # --------------------
    # Gráfico de barras apiladas
    # --------------------
    st.subheader("Evolución del Capital (Gráfico)")
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Para cada año se muestran tres componentes:
    # 1. Balance inicial (aportado originalmente, constante para todos los años)
    # 2. Depósitos periódicos acumulados hasta ese año
    # 3. Interés total acumulado
    initial_series = [initial_balance] * len(years_list)
    deposits_series = cumulative_deposits_list
    interest_series = interest_list
    
    ax.bar(years_list, initial_series, label="Balance inicial")
    ax.bar(years_list, deposits_series, bottom=initial_series, label="Depósitos periódicos")
    bottom_interest = np.array(initial_series) + np.array(deposits_series)
    ax.bar(years_list, interest_series, bottom=bottom_interest, label="Interés total")
    
    ax.set_xlabel("Año")
    ax.set_ylabel("Cantidad (€)")
    ax.set_title("Evolución del Capital")
    ax.legend()
    
    st.pyplot(fig)
