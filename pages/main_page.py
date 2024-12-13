import streamlit as st
import yaml

with open("config.yaml", "r", encoding="utf-8") as file:
    data = yaml.safe_load(file)

# Чтение данных из конфигурации
show_license = data.get('License', {}).get('show_license', False)

if show_license is True:
    st.switch_page('webUI.py')

st.write(
    "Добро пожаловать в *_numbers*! Это главное навигационное меню, от сюда вы можете выбрать нужную вам опцию. Также вы можете выбрать нужную функцию в боковой панели.")
st.page_link("webUI.py", label="License")
st.page_link("pages/cyclic_codes.py", label="Циклические коды")