import streamlit as st
import streamlit.components.v1 as components
import shutil

# Caminho da imagem
image_path = "C:/Users/greee/Downloads/EquiView360-main/EquiView360-main/static/example.jpg"

# Copiar a imagem para o mesmo diretório do HTML
shutil.copy(image_path, "example.jpg")

# Incorporar o HTML no Streamlit
html_file = "360viewer.html"

with open(html_file, 'r') as f:
    html_code = f.read()

components.html(html_code, height=600)
