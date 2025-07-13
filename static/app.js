// Get references to elements
const animalSelect = document.getElementById('animal-select');
const numPicturesInput = document.getElementById('num-pictures-input'); 
const resultImage = document.getElementById('result-image');
const resultData = document.getElementById('result-data');

// Fetch pictures and update 
async function updatePicture(url, options = {}) {
    const response = await fetch(url, options);
    const data = await response.json();

    // The data structure is different for each endpoint 
    const pictureData = Array.isArray(data) ? data[0] : data;

    // Show the first picture 
    if (pictureData) {
        resultImage.src = pictureData.url;
    }

    // Show the JSON response 
    resultData.textContent = JSON.stringify(data, null, 2);
}

// Event listener for "Get Last Picture"
document.getElementById('get-last-btn').addEventListener('click', () => {
    const animal = animalSelect.value;
    updatePicture(`/pictures/last/?animal_type=${animal}`);
});

// Event listener for "Fetch New Pictures"
document.getElementById('fetch-new-btn').addEventListener('click', () => {
    const animal = animalSelect.value;
    const num = numPicturesInput.value; 

    // Build the URL with both parameters
    const url = `/pictures/fetch/?animal_type=${animal}&num_pictures=${num}`;
    
    updatePicture(url, { method: 'POST' });
});