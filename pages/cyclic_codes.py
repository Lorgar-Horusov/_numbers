import streamlit as st
from CorrectionCodes import CodesDequallyTree

def process_coding(gx, d):
    code = CodesDequallyTree()
    k = len(gx)
    m = code.calculate_m(k)
    selected_polynomial = code.select_polynomial(m, d)
    px_binary = code.polynomial_to_binary_string(selected_polynomial)
    results = code.construct_cyclic_code(gx, m, px_binary)
    return results

def check_errors_highlight(fx_generated, fx_input):
    if len(fx_generated) != len(fx_input):
        return "Длина F(x) не совпадает с длиной введенного F(x)."
    highlighted = []
    for gen, inp in zip(fx_generated, fx_input):
        if gen != inp:
            highlighted.append(f":red[{inp}]")
        else:
            highlighted.append(str(gen))
    return "".join(highlighted)



st.write('Данное окно предоставляет доступ к инструментарию для работы с циклическими кодами при d=3, d=4')
st.write('Для начала работы выберите нужный вам метод')

col1, col2 = st.columns(2)
with col1:
    method = st.selectbox(
        "Выберите инструмент",
        ("Кодировка", "Поиск ошибок"),
        placeholder="Выберите инструмент",
    )

    if method == "Кодировка":
        with col2:
            d = st.radio("Выберите чему равен d", ("3", "4"))
            if d == "3":
                gx = st.text_input("Введите G(x)", placeholder="1101")
                if st.button("Подтвердить"):
                    if not set(gx).issubset({"0", "1"}):
                        st.write("Некорректный ввод: G(x) должен содержать только 0 и 1.")
                    else:
                        results = process_coding(gx, 3)
                        st.write("Результаты:")
                        st.latex(f'G(x) * x^m = {results["Gx_xm_binary"]}')
                        st.latex(f'Q(x) = {results["Qx_binary"]}')
                        st.latex(f'R(x) = {results["Rx_binary"]}')
                        st.latex(f'F(x) = {results["Fx_binary"]}')
                        st.latex(f'P(x) * Q(x) = {results["PQ_binary"]}')
            elif d == "4":
                st.write("Coming soon")

    elif method == "Поиск ошибок":
        with col2:
            d = st.radio("Выберите чему равен d", ("3", "4"))
            if d == "3":
                gx = st.text_input("Введите G(x)", placeholder="1101")
                fx = st.text_input("Введите F(x)", placeholder="1100010")
                if st.button("Подтвердить"):
                    if not (set(gx).issubset({"0", "1"}) and set(fx).issubset({"0", "1"})):
                        st.write("Некорректный ввод: G(x) и F(x) должны содержать только 0 и 1.")
                    else:
                        results = process_coding(gx, 3)
                        pq = results["PQ_binary"]
                        error_message = check_errors_highlight(results["Fx_binary"], fx)
                        st.markdown(pq)
                        st.markdown(error_message)
            elif d == "4":
                st.write("Coming soon")
