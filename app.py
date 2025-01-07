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

# Crear carpetas si no existen
os.makedirs('classified/yes', exist_ok=True)
os.makedirs('classified/no', exist_ok=True)
os.makedirs('classified/not_bread', exist_ok=True)
os.makedirs('classified/skipped', exist_ok=True)
os.makedirs('classified/repeated', exist_ok=True)
os.makedirs('classified/pastry', exist_ok=True)  # Nueva carpeta para bollería

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/list_images')
def list_images():
    images = os.listdir(IMAGES_FOLDER)
    return jsonify(images)

@app.route('/move_file', methods=['POST'])
def move_file():
    data = request.get_json()
    source = data['source']
    destination = data['destination']

    try:
        os.makedirs(os.path.dirname(destination), exist_ok=True)
        shutil.move(source, destination)
        return jsonify({"message": "Archivo movido correctamente."}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/restore_file', methods=['POST'])
def restore_file():
    data = request.get_json()
    source = data['source']
    destination = data['destination']

    try:
        os.makedirs(os.path.dirname(destination), exist_ok=True)
        shutil.move(source, destination)
        return jsonify({"message": "Archivo restaurado correctamente."}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/images/<filename>')
def serve_image(filename):
    return send_from_directory(IMAGES_FOLDER, filename)

if __name__ == '__main__':
    app.run(debug=True)
