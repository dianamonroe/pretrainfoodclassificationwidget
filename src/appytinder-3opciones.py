import streamlit as st
import os
from PIL import Image

# Configuración de directorios
BASE_DIR = os.path.abspath(".")
CLASSIFY_DIR = os.path.join(BASE_DIR, "data/Images_to_Classify/Bread_Images_to_classify")
NO_ES_PAN = os.path.join(BASE_DIR, "data/classified/NO_Bread")
YES_DIR = os.path.join(BASE_DIR, "data/classified/Yes_Sourdough_Bread")
NO_DIR = os.path.join(BASE_DIR, "data/classified/No_Sourdough_Bread")

# Crear carpetas de destino si no existen
os.makedirs(YES_DIR, exist_ok=True)
os.makedirs(NO_DIR, exist_ok=True)
os.makedirs(NO_ES_PAN, exist_ok=True)


# Obtener una lista de las imágenes en la carpeta CLASSIFY_DIR
images_to_classify = [f for f in os.listdir(CLASSIFY_DIR) if f.endswith(('.jpg', '.jpeg', '.png'))]

# Iniciar variables de estado
if 'current_image_index' not in st.session_state:
    st.session_state['current_image_index'] = 0

def load_image():
    """Carga la imagen actual según el índice."""
    if len(images_to_classify) > 0:
        img_path = os.path.join(CLASSIFY_DIR, images_to_classify[st.session_state['current_image_index']])
        return Image.open(img_path)
    return None

def move_image(destination_dir):
    """Mueve la imagen actual al directorio especificado y avanza a la siguiente."""
    if len(images_to_classify) > 0:
        img_name = images_to_classify[st.session_state['current_image_index']]
        img_path = os.path.join(CLASSIFY_DIR, img_name)
        os.rename(img_path, os.path.join(destination_dir, img_name))

        # Avanzar al siguiente índice
        st.session_state['current_image_index'] += 1
        if st.session_state['current_image_index'] >= len(images_to_classify):
            st.session_state['current_image_index'] = 0  # Volver al inicio si se completaron todas

def go_to_previous_image():
    """Retrocede al índice de la imagen previa."""
    if st.session_state['current_image_index'] > 0:
        st.session_state['current_image_index'] -= 1
    else:
        st.warning("Ya estás en la primera imagen.")

# Mostrar la imagen actual
image = load_image()
if image:
    st.image(image, caption=f"Imagen {st.session_state['current_image_index'] + 1}", use_column_width=True)
else:
    st.info("No hay imágenes para clasificar. Por favor, añade más imágenes a la carpeta.")

# Controles de clasificación
col1, col2, col3, col4 = st.columns([1, 1, 1, 1])

with col1:
    if st.button("❌ No Sourdough Bread"):
        move_image(NO_DIR)

with col2:
    if st.button("↩️ Volver atrás", help="Regresar a la imagen anterior"):
        go_to_previous_image()

with col3:
    if st.button("⬇️ No es pan"):
        move_image(NO_ES_PAN)

with col4:
    if st.button("❤️ Yes Sourdough Bread"):
        move_image(YES_DIR)
        
# Mensaje para cuando no hay más imágenes
if len(images_to_classify) == 0:
    st.info("No hay imágenes para clasificar. Por favor, añade más imágenes a la carpeta.")