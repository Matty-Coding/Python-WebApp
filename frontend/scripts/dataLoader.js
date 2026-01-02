// Variabile Globale per Caching dei dati
let data = null;

document.addEventListener("DOMContentLoaded", async () => {
    // Controllo per verificare presenza dati già caricati nel sessionStorage
    if (sessionStorage.getItem("data") === null) data = await getData(); 
    else data = JSON.parse(sessionStorage.getItem("data"));

    // Caricamento del contenuto dinamico
    displayData(data);

    document.dispatchEvent(new CustomEvent("dataLoaded", { detail: data }));
})

// Funzione asincrona per il fetching dei dati
async function getData() {
    const response = await fetch("assets/united_kingdom_data.json");
    data = await response.json();
    sessionStorage.setItem("data", JSON.stringify(data));
    return data;
}

// Funzione per caricare i dati dinamicamente nel DOM
function displayData(data) {
    const cardsContainer = document.querySelector("#cards-container");
    cardsContainer.innerHTML = "";

    for (const [id, champ] of Object.entries(data)) {

        const card = document.createElement("article");
        card.classList.add("card");
        card.dataset.id = id;
        
        card.innerHTML = `
            <div class="img-container">
                <img src="${champ.skins[0].splash}" alt="${champ.name} default skin">
            </div>
            <div class="name-container">
                <h2>${champ.name}</h2>
                <p>${champ.nickname}</p>
            </div>
        `;
        
        cardsContainer.appendChild(card);
    }   
}
