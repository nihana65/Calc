import streamlit as st

st.set_page_config(page_title="Calculator", page_icon="🧮", layout="centered")

st.title("🧮 Calculator")

col1, col2, col3 = st.columns([2, 1, 2])
with col1:
    a = st.number_input("First number", value=0.0, format="%g")
with col2:
    op = st.selectbox("Operator", ["+", "-", "×", "÷"])
with col3:
    b = st.number_input("Second number", value=0.0, format="%g")

if st.button("Calculate", type="primary", use_container_width=True):
    if op == "+":
        result = a + b
    elif op == "-":
        result = a - b
    elif op == "×":
        result = a * b
    elif b == 0:
        st.error("Can't divide by zero.")
        st.stop()
    else:
        result = a / b

    st.metric("Result", f"{result:,.10g}")
