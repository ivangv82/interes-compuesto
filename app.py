import streamlit as st
import math
import numpy as np

st.title("Calculadora de Ahorro y Objetivos")

# -------------------------------
# Selección de la pregunta a responder
# -------------------------------
operation = st.selectbox(
    "Selecciona la pregunta a responder:",
    [
        "¿Cuánto puedo ahorrar?",
        "¿Cuánto tardaré en alcanzar mi objetivo de ahorro?",
        "¿Cuánto necesito ahorrar en cada período para lograr mi objetivo de ahorro?",
        "¿Qué porcentaje de interés necesito para llegar a mi objetivo de ahorro?"
    ]
)

# -------------------------------
# Parámetros comunes: frecuencia y momento del depósito
# -------------------------------
frequency_option = st.selectbox("Frecuencia de depósito", 
    options=["Semanalmente", "Bi-semanalmente", "Mensualmente", "Anualmente"])
if frequency_option == "Semanalmente":
    m = 52
elif frequency_option == "Bi-semanalmente":
    m = 26
elif frequency_option == "Mensualmente":
    m = 12
elif frequency_option == "Anualmente":
    m = 1

timing_option = st.selectbox("Momento del depósito", 
    options=["Inicio del período", "Final del período"])

# -------------------------------
# Según la operación, se muestran otros campos de entrada
# -------------------------------

if operation == "¿Cuánto puedo ahorrar?":
    st.subheader("Parámetros para calcular el ahorro acumulado")
    PV = st.number_input("Balance inicial (€)", value=1000.00, format="%.2f")
    PMT = st.number_input("Depósito periódico (€)", value=100.00, format="%.2f")
    annual_rate = st.number_input("Ratio de interés anual (%)", value=1.0, step=0.1)
    years = st.number_input("Duración (años)", value=10, step=1)
    
    if st.button("Calcular"):
        i = (annual_rate / 100) / m  # tasa periódica
        n = years * m  # número total de períodos
        if i == 0:
            # Si no hay interés, el crecimiento es lineal
            FV = PV + PMT * n
        else:
            if timing_option == "Final del período":
                FV = PV * (1 + i) ** n + PMT * (((1 + i) ** n - 1) / i)
            else:  # Depósitos al inicio del período
                FV = PV * (1 + i) ** n + PMT * (((1 + i) ** n - 1) / i) * (1 + i)
        st.subheader("Resultado")
        st.write(f"El balance final será: **{FV:,.2f} €**")

elif operation == "¿Cuánto tardaré en alcanzar mi objetivo de ahorro?":
    st.subheader("Parámetros para calcular el tiempo necesario")
    PV = st.number_input("Balance inicial (€)", value=1000.00, format="%.2f")
    PMT = st.number_input("Depósito periódico (€)", value=100.00, format="%.2f")
    annual_rate = st.number_input("Ratio de interés anual (%)", value=1.0, step=0.1)
    target = st.number_input("Objetivo de ahorro (€)", value=2000.00, format="%.2f")
    
    if st.button("Calcular"):
        i = (annual_rate / 100) / m
        # Caso sin interés
        if i == 0:
            if PMT == 0:
                st.error("Con 0 interés y 0 depósito periódico, no se puede alcanzar el objetivo.")
            else:
                n = (target - PV) / PMT
        else:
            try:
                if timing_option == "Final del período":
                    # Ecuación: FV = PV*(1+i)^n + PMT*((1+i)^n - 1)/i
                    n = math.log((target + PMT / i) / (PV + PMT / i)) / math.log(1 + i)
                else:
                    # Depósitos al inicio: FV = PV*(1+i)^n + PMT*(1+i)*((1+i)^n - 1)/i
                    n = math.log((target + PMT * (1 + i) / i) / (PV + PMT * (1 + i) / i)) / math.log(1 + i)
            except Exception as e:
                st.error("Error en el cálculo. Revisa los valores ingresados.")
                n = None
        if n is not None:
            years_needed = n / m
            st.subheader("Resultado")
            st.write(f"Se necesitarán aproximadamente **{n:,.1f} períodos** (equivalentes a **{years_needed:,.2f} años**) para alcanzar tu objetivo.")

elif operation == "¿Cuánto necesito ahorrar en cada período para lograr mi objetivo de ahorro?":
    st.subheader("Parámetros para calcular el depósito periódico requerido")
    PV = st.number_input("Balance inicial (€)", value=1000.00, format="%.2f")
    annual_rate = st.number_input("Ratio de interés anual (%)", value=1.0, step=0.1)
    years = st.number_input("Duración (años)", value=10, step=1)
    target = st.number_input("Objetivo de ahorro (€)", value=2000.00, format="%.2f")
    
    if st.button("Calcular"):
        i = (annual_rate / 100) / m
        n = years * m
        if i == 0:
            # Crecimiento lineal: PMT = (target - PV) / n
            PMT_required = (target - PV) / n
        else:
            if timing_option == "Final del período":
                PMT_required = (target - PV * (1 + i) ** n) * i / ((1 + i) ** n - 1)
            else:
                PMT_required = (target - PV * (1 + i) ** n) * i / (((1 + i) ** n - 1) * (1 + i))
        st.subheader("Resultado")
        st.write(f"Necesitas depositar aproximadamente **{PMT_required:,.2f} €** en cada período.")

elif operation == "¿Qué porcentaje de interés necesito para llegar a mi objetivo de ahorro?":
    st.subheader("Parámetros para calcular el interés requerido")
    PV = st.number_input("Balance inicial (€)", value=1000.00, format="%.2f")
    PMT = st.number_input("Depósito periódico (€)", value=100.00, format="%.2f")
    years = st.number_input("Duración (años)", value=10, step=1)
    target = st.number_input("Objetivo de ahorro (€)", value=2000.00, format="%.2f")
    
    if st.button("Calcular"):
        n = years * m
        
        # Definimos la función f(i) para la tasa periódica i que queremos hallar
        def f(i):
            if i == 0:
                # Crecimiento lineal
                return PV + PMT * n - target
            if timing_option == "Final del período":
                return PV * (1 + i) ** n + PMT * (((1 + i) ** n - 1) / i) - target
            else:
                return PV * (1 + i) ** n + PMT * (1 + i) * (((1 + i) ** n - 1) / i) - target
        
        # Método de bisección para hallar i en el intervalo [low, high]
        low = 1e-8
        high = 1.0  # Tasa periódica máxima (100% por período)
        
        # Verificamos que f(low) y f(high) tengan signos opuestos
        if f(low) * f(high) > 0:
            st.error("No se encontró una solución en el rango considerado. Revisa los valores.")
        else:
            for _ in range(100):
                mid = (low + high) / 2
                if abs(f(mid)) < 1e-6:
                    break
                if f(low) * f(mid) < 0:
                    high = mid
                else:
                    low = mid
            i_solution = mid
            # Convertimos la tasa periódica a tasa anual en porcentaje:
            annual_rate_required = i_solution * m * 100
            st.subheader("Resultado")
            st.write(f"Necesitas un interés anual aproximado de **{annual_rate_required:,.2f} %** para alcanzar tu objetivo.")

