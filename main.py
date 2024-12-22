import os

# Путь к webUI.py
script_path = os.path.join(os.path.dirname(__file__), "webUI.py")

# Запуск Streamlit
os.system(f'python -m streamlit run "{script_path}"')
