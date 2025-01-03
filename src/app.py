import streamlit as st
import os
from PIL import Image
import shutil

# Configuración inicial
BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # Ruta base del archivo actual
CLASSIFY_DIR = os.path.join(BASE_DIR, "/workspaces/pretrainfoodclassificationwidget/data/Images_to_Classify/Bread Images to classify")
YES_DIR = os.path.join(BASE_DIR, "data/classified/Yes_Sourdough_Bread")
NO_DIR = os.path.join(BASE_DIR, "data/classified/No_Sourdough_Bread")


# Crear carpetas de destino si no existen
os.makedirs(YES_DIR, exist_ok=True)
os.makedirs(NO_DIR, exist_ok=True)

# Obtener la lista de imágenes por clasificar
image_files = [f for f in os.listdir(CLASSIFY_DIR) if f.lower().endswith(('.jpg', '.png'))]

# Estado inicial de la app
if "current_index" not in st.session_state:
    st.session_state.current_index = 0

# Función para mover imágenes
def move_image(file_name, destination_dir):
    source_path = os.path.join(CLASSIFY_DIR, file_name)
    dest_path = os.path.join(destination_dir, file_name)
    shutil.move(source_path, dest_path)
    st.success(f"Imagen '{file_name}' movida a '{destination_dir}'.")

# Mostrar imagen actual
if st.session_state.current_index < len(image_files):
    current_image = image_files[st.session_state.current_index]
    current_image_path = os.path.join(CLASSIFY_DIR, current_image)
    
    # Mostrar imagen
    st.image(Image.open(current_image_path), caption=f"Clasificando: {current_image}", use_column_width=True)
    
    # Botones de clasificación
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Swipe Right: Pan por encima del 90% masa madre"):
            move_image(current_image, YES_DIR)
            st.session_state.current_index += 1  # Pasar a la siguiente imagen
    with col2:
        if st.button("Swipe Left: Pan por debajo del 90% masa madre"):
            move_image(current_image, NO_DIR)
            st.session_state.current_index += 1  # Pasar a la siguiente imagen
else:
    st.success("¡Has clasificado todas las imágenes!")
    st.balloons()

# Mostrar progreso
st.sidebar.write(f"Progreso: {st.session_state.current_index}/{len(image_files)} imágenes clasificadas.")
