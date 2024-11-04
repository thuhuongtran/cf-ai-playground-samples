import importlib.util

import streamlit as st


def load_module_from_path(module_name, file_path):
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


pages = {
    "Text Generation": "TextGen.py",
    "Translation": "Translate.py",
    "Code Generation": "CodeGen.py",
    "Tests & Debug": "TestAndDebug.py",
}

st.sidebar.title("Navigation")
selection = st.sidebar.radio("Go to", list(pages.keys()))

page_path = pages[selection]
load_module_from_path(selection, page_path)
