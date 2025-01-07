const imagesFolder = "./images/";
const classifiedFolders = {
    yes: "./classified/yes/",
    no: "./classified/no/",
    not_bread: "./classified/not_bread/",
    skipped: "./classified/skipped/",
    repeated: "./classified/repeated/",
    pastry: "./classified/pastry/" // Nueva carpeta para bollería
};

let images = [];
let currentIndex = 0;
let history = [];

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

function classify(category) {
    if (currentIndex < images.length) {
        const imageName = images[currentIndex];
        moveFile(imagesFolder + imageName, classifiedFolders[category] + imageName);
        history.push(currentIndex);
        currentIndex++;
        showImage();
    }
}

function goBack() {
    if (history.length > 0) {
        currentIndex = history.pop();
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
