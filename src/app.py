import os
import random
import git
import streamlit as st
from PIL import Image

# Directorios y configuración
BASE_DIR = os.path.abspath(".")
CLASSIFY_DIR = os.path.join(BASE_DIR, "data/Images_to_Classify/Bread_Images_to_classify")
YES_DIR = os.path.join(BASE_DIR, "data/classified/Yes_Sourdough_Bread")
NO_DIR = os.path.join(BASE_DIR, "data/classified/No_Sourdough_Bread")
NO_ES_PAN = os.path.join(BASE_DIR, "data/classified/NO_Bread")

# Crear carpetas de destino si no existen
os.makedirs(YES_DIR, exist_ok=True)
os.makedirs(NO_DIR, exist_ok=True)
os.makedirs(NO_ES_PAN, exist_ok=True)

# Función para mover imagen
def move_image(image_file, target_dir):
    try:
        # Mover imagen
        os.rename(os.path.join(CLASSIFY_DIR, image_file), os.path.join(target_dir, image_file))
        # Realizar commit y push al repositorio
        repo = git.Repo(BASE_DIR)
        repo.git.add(os.path.join(target_dir, image_file))  # Añadir archivo al staging area
        repo.index.commit(f"Clasificada imagen {image_file}")  # Crear commit
        repo.git.push()  # Hacer push a GitHub
        st.success(f"Imagen {image_file} movida a {target_dir} y cambios subidos a GitHub.")
    except Exception as e:
        st.error(f"Error al mover la imagen {image_file}: {e}")

# Cargar las imágenes
image_files = os.listdir(CLASSIFY_DIR)
image_files = [file for file in image_files if file.endswith(('jpg', 'png', 'jpeg'))]  # Filtrar solo imágenes

# Función para mostrar imagen y clasificación
def show_image_to_classify(image_path):
    image = Image.open(image_path)
    st.image(image, caption='¿Esto es pan con más de 90% de masa madre?', use_container_width=True)

# Título y subtítulo
st.markdown("""
    <div style="text-align: center; margin-bottom: 30px;">
        <h1>¿Esto es pan con más de 90% de masa madre?</h1>
        <p>Desliza a la izquierda la foto si crees que <b>NO</b> o a la derecha si crees que <b>SÍ</b>.</p>
    </div>
""", unsafe_allow_html=True)

# Función de clasificación
def classify_bread(image_file, action):
    if action == "Sí":
        st.write("¡Clasificado como pan de masa madre!")
        move_image(image_file, YES_DIR)  # Mover imagen a la carpeta correspondiente
    elif action == "No":
        st.write("¡Clasificado como no pan de masa madre!")
        move_image(image_file, NO_DIR)  # Mover imagen a la carpeta correspondiente
    elif action == "No es Pan":
        st.write("¡Clasificado como no es pan!")
        move_image(image_file, NO_ES_PAN)  # Mover imagen a la carpeta correspondiente

# Interacción de swipe (simulada con botones)
if image_files:
    current_image = random.choice(image_files)  # Seleccionar una imagen aleatoria de la lista
    show_image_to_classify(os.path.join(CLASSIFY_DIR, current_image))

    col1, col2, col3 = st.columns([1, 3, 1])
    with col1:
        swipe_left = st.button("No Pan")
    with col2:
        swipe_right = st.button("Sí Pan")
    with col3:
        swipe_down = st.button("No es Pan")

    # Procesar clasificación
    if swipe_left:
        classify_bread(current_image, "No")
        image_files.remove(current_image)  # Eliminar imagen clasificada
    elif swipe_right:
        classify_bread(current_image, "Sí")
        image_files.remove(current_image)  # Eliminar imagen clasificada
    elif swipe_down:
        classify_bread(current_image, "No es Pan")
        image_files.remove(current_image)  # Eliminar imagen clasificada

    # Cargar siguiente imagen automáticamente
    if image_files:
        current_image = random.choice(image_files)  # Elegir una nueva imagen aleatoria
        show_image_to_classify(os.path.join(CLASSIFY_DIR, current_image))

else:
    st.write("¡No hay más imágenes para clasificar!")
