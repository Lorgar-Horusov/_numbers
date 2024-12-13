import streamlit as st
from CorrectionCodes import CodesDequallyTree
import yaml

with open("config.yaml", "r", encoding="utf-8") as file:
    data = yaml.safe_load(file)

# Чтение данных из конфигурации
show_license = data.get('License', {}).get('show_license', False)

if show_license is True:
    st.switch_page('webUI.py')

def process_coding(gx, d):
    """
    Обрабатывает кодирование на основе заданного G(x) и d.
    """
    code = CodesDequallyTree()
    k = len(gx)
    m = code.calculate_m(k)
    selected_polynomial = code.select_polynomial(m, d)
    px_binary = code.polynomial_to_binary_string(selected_polynomial)
    results = code.construct_cyclic_code(gx, m, px_binary)
    return results

def check_errors_highlight(fx_generated, fx_input):
    """
    Проверяет ошибки и выделяет их в тексте.
    """
    if len(fx_generated) != len(fx_input):
        return "Длина F(x) не совпадает с длиной введенного F(x)."
    highlighted = [
        f":red[{inp}]" if gen != inp else str(gen)
        for gen, inp in zip(fx_generated, fx_input)
    ]
    return "".join(highlighted)

# Заголовок страницы
st.title("Инструментарий для работы с циклическими кодами")
st.write(
    """
    Это приложение предоставляет доступ к работе с циклическими кодами для d=3, d=4.
    Выберите нужный метод для начала.
    """
)

# Выбор метода
method = st.selectbox(
    "Выберите инструмент", ["Кодировка", "Поиск ошибок"], index=0, placeholder="Выберите инструмент"
)

# Выбор параметров в зависимости от метода
if method == "Кодировка":
    d = st.radio("Выберите значение d", ["3", "4"], index=0)
    gx = st.text_input("Введите G(x)", placeholder="1101")

    if st.button("Подтвердить"):
        if not set(gx).issubset({"0", "1"}):
            st.error("Некорректный ввод: G(x) должен содержать только 0 и 1.")
        else:
            results = process_coding(gx, int(d))
            st.subheader("Результаты:")
            st.latex(f'G(x) * x^m = {results["Gx_xm_binary"]}')
            st.latex(f'Q(x) = {results["Qx_binary"]}')
            st.latex(f'R(x) = {results["Rx_binary"]}')
            st.latex(f'F(x) = {results["Fx_binary"]}')
            st.latex(f'P(x) * Q(x) = {results["PQ_binary"]}')

elif method == "Поиск ошибок":
    d = st.radio("Выберите значение d", ["3", "4"], index=0)
    gx = st.text_input("Введите G(x)", placeholder="1101")
    fx = st.text_input("Введите F(x)", placeholder="1100010")

    if st.button("Подтвердить"):
        if not (set(gx).issubset({"0", "1"}) and set(fx).issubset({"0", "1"})):
            st.error("Некорректный ввод: G(x) и F(x) должны содержать только 0 и 1.")
        else:
            results = process_coding(gx, int(d))
            pq = results["PQ_binary"]
            error_message = check_errors_highlight(results["Fx_binary"], fx)

            st.subheader("Результаты:")
            st.markdown(f"**P(x) * Q(x):** {pq}")
            st.markdown(f"**Ошибки в F(x):** {error_message}")

else:
    st.info("Выберите инструмент для начала работы.")
