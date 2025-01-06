import os
import random
import git
import streamlit as st
from PIL import Image
from dotenv import load_dotenv


from dotenv import load_dotenv
import os

# Cargar las variables de entorno desde el archivo .env
load_dotenv(dotenv_path=os.path.join(os.path.dirname("/workspaces/pretrainfoodclassificationwidget/src"), '.env'))

# Obtener el token de GitHub desde la variable de entorno
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

# Verificar si el token de GitHub está cargado correctamente
if not GITHUB_TOKEN:
    raise ValueError("El token de GitHub no está definido. Asegúrate de que esté en tu archivo .env")

print("Token cargado correctamente")


# Directorios y configuración
BASE_DIR = os.path.abspath(".")
CLASSIFY_DIR = os.path.join(BASE_DIR, "src/data/Images_to_Classify/Bread_Images_to_classify")
YES_DIR = os.path.join(BASE_DIR, "src/data/classified/Yes_Sourdough_Bread")
NO_DIR = os.path.join(BASE_DIR, "src/data/classified/No_Sourdough_Bread")
NO_ES_PAN = os.path.join(BASE_DIR, "src/data/classified/NO_Bread")



# Crear carpetas de destino si no existen
os.makedirs(YES_DIR, exist_ok=True)
os.makedirs(NO_DIR, exist_ok=True)
os.makedirs(NO_ES_PAN, exist_ok=True)

# Función para mover imagen
def move_image(image_file, target_dir):
    try:
        # Mover imagen
        os.rename(os.path.join(CLASSIFY_DIR, image_file), os.path.join(target_dir, image_file))

        # Crear un objeto repo que apunta al directorio base de tu repositorio
        repo = git.Repo(BASE_DIR)

        # Añadir el archivo movido al staging area
        repo.git.add(os.path.join(target_dir, image_file))

        # Crear commit
        repo.index.commit(f"Clasificada imagen {image_file}")

        # Realizar push al repositorio usando el token de GitHub
        repo.git.push(f"https://{GITHUB_TOKEN}@github.com/dianamonroe/pretrainfoodclassificationwidget.git")

        # Mensaje de éxito
        print(f"Imagen {image_file} movida a {target_dir} y cambios subidos a GitHub.")

    except Exception as e:
        print(f"Error al mover la imagen {image_file}: {e}")

# Cargar las imágenes
image_files = os.listdir(CLASSIFY_DIR)
image_files = [file for file in image_files if file.endswith(('jpg', 'png', 'jpeg'))]  # Filtrar solo imágenes

# Inicializar el índice de la imagen
if 'current_index' not in st.session_state:
    st.session_state.current_index = 0

# Función para mostrar la imagen actual
def show_image_to_classify():
    if st.session_state.current_index < len(image_files):
        current_image = image_files[st.session_state.current_index]
        current_image_path = os.path.join(CLASSIFY_DIR, current_image)
        st.image(Image.open(current_image_path), use_container_width=True, caption=None)

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
        st.write("¡Clasificado como pan 100% masa madre!")
        move_image(image_file, YES_DIR)  # Mover imagen a la carpeta correspondiente
    elif action == "No":
        st.write("¡Clasificado como no es pan 100% masa madre!")
        move_image(image_file, NO_DIR)  # Mover imagen a la carpeta correspondiente
    elif action == "No es Pan":
        st.write("¡Clasificado como no es pan!")
        move_image(image_file, NO_ES_PAN)  # Mover imagen a la carpeta correspondiente

# Botones de clasificación
col1, col2, col3 = st.columns([1, 3, 1])
with col1:
    swipe_left = st.button("No")
with col2:
    swipe_right = st.button("Sí")
with col3:
    swipe_down = st.button("No es Pan")

# Procesar clasificación
if st.session_state.current_index < len(image_files):
    current_image = image_files[st.session_state.current_index]
    
    if swipe_left:
        classify_bread(current_image, "No")
        st.session_state.current_index += 1  # Avanzar al siguiente índice de imagen
    elif swipe_right:
        classify_bread(current_image, "Sí")
        st.session_state.current_index += 1  # Avanzar al siguiente índice de imagen
    elif swipe_down:
        classify_bread(current_image, "No es Pan")
        st.session_state.current_index += 1  # Avanzar al siguiente índice de imagen

# Mostrar la imagen actual
show_image_to_classify()

# Mostrar mensaje si no hay más imágenes
if st.session_state.current_index >= len(image_files):
    st.write("¡No hay más imágenes para clasificar!")

# Realizar push final a GitHub para subir todos los cambios
repo = git.Repo(BASE_DIR)
repo.git.push(f"https://{GITHUB_TOKEN}@github.com/dianamonroe/pretrainfoodclassificationwidget.git")

