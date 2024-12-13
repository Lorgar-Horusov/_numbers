import streamlit as st
from CorrectionCodes import HammingCodes
import yaml

with open("config.yaml", "r", encoding="utf-8") as file:
    data = yaml.safe_load(file)

# Чтение данных из конфигурации
show_license = data.get('License', {}).get('show_license', False)

if show_license is True:
    st.switch_page('webUI.py')

st.title("Инструментарий для работы с кодами Хейминга")
st.write(
    """
    Это приложение предоставляет доступ к работе с кодами Хейминга для d=3
    Выберите нужный метод для начала.
    """
)

method = st.selectbox(
    "Выберите инструмент", ["Кодировка", "Поиск ошибок"], index=0, placeholder="Выберите инструмент"
)

if method == "Кодировка":
    k = st.text_input("Введите k", placeholder="1101")

    if st.button("Подтвердить"):
        if not set(k).issubset({"0", "1"}):
            st.error("Некорректный ввод: G(x) должен содержать только 0 и 1.")
        else:
            binary_list = list(map(int, k))
            hamming = HammingCodes()
            hamming_m = hamming.calculate_m(*binary_list)
            hamming_mk = hamming.complectate_mk(binary_list, hamming_m)
            st.write(f"m = {hamming_m}")
            st.write(f"mk = {hamming_mk}")
