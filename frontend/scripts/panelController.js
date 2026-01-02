document.addEventListener("DOMContentLoaded", () => new PanelController());

class PanelController {
    constructor() {
        this.cardsContainer = document.querySelector("#cards-container");
        this.panel = document.querySelector(".panel");
        this.isOpen = false;
        this.currentID = null;
        this.ids = null;
        this.champ = null;
        this.skins = null;
        this.currentSkinIndex = null;
        this.loader();
    }

    loader() {
        document.addEventListener("cardSelected", e => {
            this.currentID = e.detail.id;
            this.ids = e.detail.ids;

            if (!this.isOpen) {
                this.isOpen = true;
                this.open();
            } else {
                this.updateChamp();
            }
        });

        document.addEventListener("currentChamp", e => {
            this.champ = e.detail;
            this.rendering();
        });

        document.addEventListener("keydown", e => {
            if (this.isOpen) {
                switch (e.key) {
                    case "ArrowLeft":
                        this.prevSkin();
                        break;
                    case "ArrowRight":
                        this.nextSkin();
                        break;
                    case "ArrowUp":
                        e.preventDefault();
                        this.prevChamp();
                        break;
                    case "ArrowDown":
                        e.preventDefault();
                        this.nextChamp();
                        break;
                    case "Escape":
                        this.close();
                        break;
                }
            }
        });

        document.addEventListener("selectedCardClosed", () => this.close());
    }

    open() {
        this.requestData();
        this.cardsContainer.classList.add("secondary");
        this.panel.classList.add("open");
    }

    updateChamp() {
        this.requestData();
    }

    requestData() {
        document.dispatchEvent(
            new CustomEvent("dataRequest", { detail: {id: this.currentID} })
        )
    }

    prevSkin() {
        if (this.currentSkinIndex === 0) {
            this.currentSkinIndex = this.skins.length - 1;
        } else {
            this.currentSkinIndex--;
        }
        this.updateSkin();
    }

    nextSkin() {
        if (this.currentSkinIndex === this.skins.length - 1) {
            this.currentSkinIndex = 0;
        } else {
            this.currentSkinIndex++;
        }
        this.updateSkin();
    }

    // Caricamento anticipato dell'immagine corrente + adicenti (sx/dx)
    preloadSkin(index) {
        if (index < 0 || index >= this.skins.length) return;
        const img = new Image();
        img.src = this.skins[index].splash;
    }

    updateSkin() {
        const currentSkin = this.skins[this.currentSkinIndex];
        const imgElement = this.panel.querySelector(".skin");
        imgElement.src = currentSkin.splash;

        this.panel
            .querySelector(".skin-name")
            .textContent = currentSkin.name === "default" ? this.champ.name : currentSkin.name;

        // Caricamento anticipato
        this.preloadSkin(this.currentSkinIndex - 1);
        this.preloadSkin(this.currentSkinIndex + 1);

        // Aggiornamento indicatore
        const indicators = this.panel.querySelectorAll(".indicators i");
        indicators.forEach((dot, idx) => {
            dot.className = idx === this.currentSkinIndex ? "bi bi-dash-lg" : "bi bi-dash";
        });

        // Aggiornamento scroll orizzontale
        const container = this.panel.querySelector(".indicators");
        const activeDot = this.panel.querySelector(".bi.bi-dash-lg");
        if (activeDot && container) {
            const containerCenter = container.offsetWidth / 2;
            const dotCenter = activeDot.offsetLeft + activeDot.offsetWidth / 2;
        
            container.scrollTo({
                left: dotCenter - containerCenter,
                behavior: "smooth"
            });
        }
    }

    prevChamp() {
        if (this.ids.indexOf(this.currentID) === 0) return;
        this.currentID = this.ids[this.ids.indexOf(this.currentID) - 1];
        this.updateChamp();
    }

    nextChamp() {
        if (this.ids.indexOf(this.currentID) === this.ids.length - 1) return;
        this.currentID = this.ids[this.ids.indexOf(this.currentID) + 1];
        this.updateChamp();
    }

    rendering() {
        this.panel.innerHTML = "";
        this.currentSkinIndex = 0;
        this.skins = Object.values(this.champ.skins);

        // Tasto per chiudere il pannello
        const buttonClose = document.createElement("button");
        buttonClose.type = "button";
        buttonClose.classList.add("close-button");

        buttonClose.addEventListener("click", () => this.close());

        const closeBtn = document.createElement("i");
        closeBtn.className = "bi bi-x-lg";

        buttonClose.appendChild(closeBtn);
        this.panel.appendChild(buttonClose);

        // Contenitore dei dettagli
        const details = document.createElement("div");
        details.classList.add("details");

        // Carosello delle skin
        const carousel = document.createElement("div");
        carousel.classList.add("carousel");

        const buttonArrowLeftSkin = document.createElement("button");
        buttonArrowLeftSkin.type = "button";
        buttonArrowLeftSkin.classList.add("arrow-button");

        const arrowLeftSkin = document.createElement("i");
        arrowLeftSkin.className = "bi bi-chevron-left";
        buttonArrowLeftSkin.appendChild(arrowLeftSkin);
        buttonArrowLeftSkin.addEventListener("click", () => this.prevSkin());
        carousel.appendChild(buttonArrowLeftSkin);

        const skinContainer = document.createElement("div");
        skinContainer.classList.add("skin-container");

        const figure = document.createElement("figure");
        const img = document.createElement("img");
        img.classList.add("skin");
        const figcaption = document.createElement("figcaption");
        figcaption.classList.add("skin-name");

        img.src = this.skins[0].splash;
        img.alt = `${this.champ.name} default skin`;
        img.loading = "lazy";
        figure.appendChild(img);
        
        figcaption.textContent = this.champ.name;
        figure.appendChild(figcaption);

        skinContainer.appendChild(figure);
        carousel.appendChild(skinContainer);

        const buttonArrowRightSkin = document.createElement("button");
        buttonArrowRightSkin.type = "button";
        buttonArrowRightSkin.classList.add("arrow-button");

        const arrowRightSkin = document.createElement("i");
        arrowRightSkin.className = "bi bi-chevron-right";
        buttonArrowRightSkin.appendChild(arrowRightSkin);
        buttonArrowRightSkin.addEventListener("click", () => this.nextSkin());
        carousel.appendChild(buttonArrowRightSkin);

        const indicators = document.createElement("div");
        indicators.classList.add("indicators");

        for (const skin of this.skins) {
            const indicator = document.createElement("i");
            if (skin.name === "default") {
                indicator.className = "bi bi-dash-lg";
                indicators.appendChild(indicator);
                continue;
            } 
            indicator.className = "bi bi-dash";
            indicators.appendChild(indicator);
        }
        carousel.appendChild(indicators);

        let touchStartX = 0;
        carousel.addEventListener("touchstart", e => {
            touchStartX = e.touches[0].clientX;
        });

        carousel.addEventListener("touchend", e => {
            const touchEndX = e.changedTouches[0].clientX;
            const deltaX = touchEndX - touchStartX;

            if (Math.abs(deltaX) > 50) {
                if (deltaX > 0) {
                    this.prevSkin();
                } else {
                    this.nextSkin();
                }
            }
        })

        details.appendChild(carousel);
        
        // Contenitore del nome con frecce direzionali
        const header = document.createElement("div");
        header.classList.add("panel-header");

        const buttonArrowLeftChamp = document.createElement("button");
        buttonArrowLeftChamp.type = "button";
        buttonArrowLeftChamp.classList.add("arrow-button");

        if (this.ids.indexOf(this.currentID) === 0) 
            buttonArrowLeftChamp.classList.add("not-allowed");
        buttonArrowLeftChamp.addEventListener("click", () => this.prevChamp());

        const arrowLeftChamp = document.createElement("i");
        arrowLeftChamp.className = "bi bi-chevron-left";
        buttonArrowLeftChamp.appendChild(arrowLeftChamp);

        const nameContainer = document.createElement("div");
        nameContainer.classList.add("name-panel-container");

        const name = document.createElement("h2");
        name.textContent = this.champ.name;

        const nickname = document.createElement("p");
        nickname.textContent = this.champ.nickname;

        nameContainer.appendChild(name);
        nameContainer.appendChild(nickname);
  
        const buttonArrowRightChamp = document.createElement("button");
        buttonArrowRightChamp.type = "button";
        buttonArrowRightChamp.classList.add("arrow-button");

        if (this.ids.indexOf(this.currentID) === this.ids.length - 1) 
            buttonArrowRightChamp.classList.add("not-allowed");
        buttonArrowRightChamp.addEventListener("click", () => this.nextChamp());

        const arrowRightChamp = document.createElement("i");
        arrowRightChamp.className = "bi bi-chevron-right";
        buttonArrowRightChamp.appendChild(arrowRightChamp);

        header.appendChild(buttonArrowLeftChamp);
        header.appendChild(nameContainer);      
        header.appendChild(buttonArrowRightChamp);

        details.appendChild(header);

        // Lista delle abilità
        const ul = document.createElement("ul");
        ul.classList.add("abilities-container");
        ul.addEventListener("click", e => {
            const abilityTitle = e.target.closest(".ability-item");
            if (!abilityTitle) return;

            const description = abilityTitle.querySelector(".ability-description");
            ul.querySelectorAll(".ability-description.open").forEach(desc => {
                if (desc !== description) desc.classList.remove("open");
            });

            description.classList.toggle("open");
        });

        for (const [key, ability] of Object.entries(this.champ.abilities)) {
            const li = document.createElement("li");
            li.classList.add("ability-item");
            
            const iconDiv = document.createElement("div");
            iconDiv.classList.add("icon-ability-container");
            
            const icon = document.createElement("img");
            icon.src = ability.icon;
            icon.alt = key;
            icon.loading = "lazy";
            iconDiv.appendChild(icon);

            const abilityText = document.createElement("div");
            abilityText.classList.add("ability-text");
            
            const abilityTitle = document.createElement("h3");
            abilityTitle.textContent = `${ability.name} ~ ${key.charAt(0).toUpperCase() + key.slice(1)}`;
        
            const abilityDescription = document.createElement("p");
            abilityDescription.classList.add("ability-description");
            abilityDescription.textContent = ability.description;

            abilityText.appendChild(abilityTitle);
            abilityText.appendChild(abilityDescription);
            
            li.appendChild(iconDiv);
            li.appendChild(abilityText);
            
            ul.appendChild(li);
        }

        details.appendChild(ul);

        this.panel.appendChild(details);
    }

    close() {
        document.dispatchEvent(new CustomEvent("panelClosed"));
        this.currentSkinIndex = null;
        this.skins = null;
        this.currentID = null;
        this.panel.classList.remove("open");
        this.cardsContainer.classList.remove("secondary");
        this.panel.innerHTML = "";
        this.isOpen = false;
    }
}