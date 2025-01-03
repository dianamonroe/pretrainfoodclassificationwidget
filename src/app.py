import streamlit as st
import os
from PIL import Image
import shutil

# Configuración inicial
BASE_DIR = os.path.abspath(".")
CLASSIFY_DIR = os.path.join(BASE_DIR, "data/Images_to_Classify/Bread_Images_to_classify")
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
    st.success(f"Imagen movida a '{destination_dir}'.")

# Función para retroceder a la imagen previa
def reload_previous():
    if st.session_state.current_index > 0:
        st.session_state.current_index -= 1
        st.info("Imagen previa cargada.")

# Interfaz principal
st.markdown(
    """
    <div style="text-align: center; margin-bottom: 30px;">
        <h1>¿Esto es pan con más de 90% de masa madre?</h1>
        <p>Desliza a la izquierda la foto si crees que <b>NO</b> o a la derecha si crees que <b>SÍ</b>.</p>
    </div>
    """, 
    unsafe_allow_html=True
)

# Mostrar imagen actual
if st.session_state.current_index < len(image_files):
    current_image = image_files[st.session_state.current_index]
    current_image_path = os.path.join(CLASSIFY_DIR, current_image)
    
    # Mostrar imagen
    st.image(Image.open(current_image_path), use_container_width=True, caption=None)
    
    # Columnas para deslizamiento
    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("⬅️ NO"):
            move_image(current_image, NO_DIR)
            st.session_state.current_index += 1  # Pasar a la siguiente imagen
    with col2:
        if st.button("➡️ SÍ"):
            move_image(current_image, YES_DIR)
            st.session_state.current_index += 1  # Pasar a la siguiente imagen

    # Botón para recargar la imagen previa
    st.button("🔄 Volver a la imagen anterior", on_click=reload_previous)

else:
    st.success("¡Has clasificado todas las imágenes!")
    st.balloons()

# Mostrar progreso
st.sidebar.write(f"Progreso: {st.session_state.current_index}/{len(image_files)} imágenes clasificadas.")



 
