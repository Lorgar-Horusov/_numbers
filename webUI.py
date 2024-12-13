import streamlit as st
from streamlit_modal import Modal
import yaml

st.title("Welcome to __Numbers_")

# Открытие конфигурационного файла
with open("config.yaml", "r", encoding="utf-8") as file:
    data = yaml.safe_load(file)

# Чтение данных из конфигурации
show_license = data.get('License', {}).get('show_license', False)
license_file = data.get('License', {}).get('license_text', "")

# Чтение содержимого LICENSE.md, если путь указан
if license_file:
    with open(license_file, "r", encoding="utf-8") as f:
        license_text = f.read()
else:
    license_text = "Лицензия не найдена."

# Создание модального окна
modal = Modal(
    "License",
    key="demo-modal",
    padding=20,
    max_width=744
)
button_activated = True
# Если в конфигурации указано показывать лицензию, открываем модальное окно
open_modal = st.button("License", disabled=button_activated)
if open_modal:
    modal.open()
elif show_license is False:
    button_activated = False
    st.write("License is accepted")
    gotu_main = st.button("Go to main")
    if gotu_main:
        st.switch_page('pages/main_page.py')
# Проверяем, открыто ли окно
if modal.is_open():
    with modal.container():
        st.markdown(license_text)

        # Добавляем чекбокс для принятия лицензии
        value = st.checkbox("accept")

        # Кнопка для закрытия модального окна
        close_button = st.button("Close")

        if value and close_button:
            data['License']['show_license'] = False
            with open("config.yaml", "w", encoding="utf-8") as file:
                yaml.dump(data, file)
            modal.close()

