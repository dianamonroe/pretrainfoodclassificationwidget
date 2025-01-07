const imagesFolder = "./images/";
const classifiedFolders = {
  yes: "./classified/yes/",
  no: "./classified/no/",
  not_bread: "./classified/not_bread/",
  skipped: "./classified/skipped/",
  repeated: "./classified/repeated/"
};

let images = [];
let currentIndex = 0;
let history = [];

// Cargar las imágenes al inicio
window.onload = async () => {
  const response = await fetch("/list_images");
  images = await response.json();
  updateRemainingImages();
  showImage();
};

function updateRemainingImages() {
  const remaining = images.length - currentIndex;
  document.getElementById("remainingImages").textContent = `Imágenes por clasificar: ${remaining}`;
}

function showImage() {
  if (currentIndex < images.length) {
    document.getElementById("currentImage").src = imagesFolder + images[currentIndex];
  } else {
    alert("¡Todas las imágenes han sido clasificadas!");
  }
  updateRemainingImages();
}

let reverseHistory = []; // Historial para revertir clasificación

function classify(category) {
    if (currentIndex < images.length) {
        const imageName = images[currentIndex];
        const source = imagesFolder + imageName;
        const destination = classifiedFolders[category] + imageName;

        moveFile(source, destination);
        history.push({ index: currentIndex, category }); // Guardar historial con categoría
        reverseHistory.push({ source: destination, destination: source }); // Guardar para deshacer

        currentIndex++;
        showImage();
    }
}

function goBack() {
  if (history.length > 0) {
      currentIndex = history.pop();
      const previousImage = images[currentIndex];
      
      // Restaurar imagen si estaba en una carpeta clasificada
      Object.values(classifiedFolders).forEach(async folder => {
          const source = folder + previousImage;
          const destination = imagesFolder + previousImage;
          try {
              await fetch("/restore_file", {
                  method: "POST",
                  headers: { "Content-Type": "application/json" },
                  body: JSON.stringify({ source, destination })
              });
          } catch (error) {
              console.error("Error restaurando la imagen:", error);
          }
      });

      showImage();
  } else {
      alert("No hay imágenes previas para volver.");
  }
}


function skip() {
  if (currentIndex < images.length) {
    const imageName = images[currentIndex];
    moveFile(imagesFolder + imageName, classifiedFolders.skipped + imageName);
    history.push(currentIndex);
    currentIndex++;
    showImage();
  }
}

async function moveFile(source, destination) {
  await fetch("/move_file", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ source, destination })
  });
}
