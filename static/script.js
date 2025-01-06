const imagesFolder = "./images/";  // Actualiza la ruta de las imágenes a clasificar
const classifiedFolders = {
  yes: "./classified/yes/",
  no: "./classified/no/",
  not_bread: "./classified/not_bread/"
};

let images = [];
let currentIndex = 0;
let history = [];

// Cargar las imágenes al inicio
window.onload = async () => {
  const response = await fetch("/list_images");  // Endpoint para listar las imágenes
  images = await response.json();
  showImage();
};

// Muestra la imagen actual
function showImage() {
  if (currentIndex < images.length) {
    document.getElementById("current-image").src = imagesFolder + images[currentIndex];
  } else {
    alert("¡Todas las imágenes han sido clasificadas!");
  }
}

// Clasifica la imagen seleccionada
function classify(category) {
  if (currentIndex < images.length) {
    const imageName = images[currentIndex];
    moveFile(imagesFolder + imageName, classifiedFolders[category] + imageName);
    history.push(currentIndex);  // Guarda el índice de la imagen clasificada
    currentIndex++;  // Avanza al siguiente índice
    showImage();  // Muestra la siguiente imagen
  }
}

// Regresa a la imagen anterior
function goBack() {
  if (history.length > 0) {
    currentIndex = history.pop();  // Retrocede al índice anterior
    showImage();
  } else {
    alert("No hay imágenes previas para volver.");
  }
}

// Simula mover el archivo (realiza una llamada POST al servidor)
async function moveFile(source, destination) {
  await fetch("/move_file", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ source, destination })
  });
}
