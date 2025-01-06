from flask import Flask, render_template, jsonify, request, send_from_directory
import os
import shutil

app = Flask(__name__)

# Definir las carpetas
IMAGES_FOLDER = '/workspace/pretrainfoodclassificationwidget/images'
CLASSIFIED_FOLDER = '/workspace/pretrainfoodclassificationwidget/classified'

# Verificar las carpetas
os.makedirs(IMAGES_FOLDER, exist_ok=True)
os.makedirs(CLASSIFIED_FOLDER, exist_ok=True)

@app.route('/')
def index():
    # Servir el archivo index.html desde la carpeta templates
    return render_template('index.html')

@app.route('/list_images')
def list_images():
    # Listar las imágenes en la carpeta de imágenes no clasificadas
    images = os.listdir(IMAGES_FOLDER)
    return jsonify(images)

@app.route('/move_file', methods=['POST'])
def move_file():
    data = request.get_json()
    source = data['source']
    destination = data['destination']

    try:
        # Asegurarse de que la carpeta de destino exista
        os.makedirs(os.path.dirname(destination), exist_ok=True)
        shutil.move(source, destination)  # Mover archivo
        return jsonify({"message": "Archivo movido correctamente."}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/images/<filename>')
def serve_image(filename):
    return send_from_directory(IMAGES_FOLDER, filename)

if __name__ == '__main__':
    app.run(debug=True)
