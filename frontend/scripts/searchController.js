// Attesa dati tramite CustomEvent
document.addEventListener("dataLoaded", e => {
    new SearchController(e.detail);
});

class SearchController {
    constructor(data) {
        this.data = data;              // data
        this.activeIndex = -1;         // nessuna selezione 
        this.inputMode = "keyboard";   // switch keyboard/mouse

        this.searchInput = document.querySelector("#search-input");
        this.resultsList = document.querySelector("#search-results");
        this.resultsBlock = document.querySelector(".results");
        this.cardsContainer = document.querySelector("#cards-container");
        this.form = this.searchInput.closest("form");

        this.loader();
    }

    // Sezione Eventi

    loader() {
        this.searchInput.addEventListener("input", e => this.onInput(e));
        this.searchInput.addEventListener("keydown", e => this.onKeydown(e));
        this.resultsList.addEventListener("click", e => this.onResultClick(e));
        this.resultsList.addEventListener("mouseleave", () => {
            if (this.inputMode === "mouse") {
                this.activeIndex = -1;
                this.updateFocus();
            }
        });        
        this.form.addEventListener("submit", e => {
            e.preventDefault();
            this.select();
        });
        this.cardsContainer.addEventListener("click", e => {
            const card = e.target.closest("article[data-id]");
            if (!card) return;
            if (card.classList.contains("selected")) {
                this.clearSelectedCards();
                document.dispatchEvent(new CustomEvent("selectedCardClosed"));
                return;
            };
            this.selectById(card.dataset.id);
        });        

        // Listener evento del pannello
        document.addEventListener("dataRequest", e => this.getData(e.detail.id));

        document.addEventListener("panelClosed", () => this.clearSelectedCards());
    }

    onInput(e) {
        const value = e.target.value.trim().toLowerCase();
        this.activeIndex = -1;
        this.inputMode = "keyboard";

        if (!value) {
            this.clearResults();
            return;
        }

        this.renderResults(value);
    }

    onKeydown(e) {
        if (!this.resultsList.children.length) return;
    
        this.inputMode = "keyboard";
    
        switch (e.key) {
            case "ArrowUp":
                this.move(-1);
                break;
            case "ArrowDown":
                this.move(1);
                break;
            case "Enter":
                e.preventDefault();
                this.select();
                break;
        }
    }
    
    onResultClick(e) {
        const li = e.target.closest("li");
        if (!li) return;

        this.selectById(li.dataset.id);
    }

    // Sezione logica 

    move(direction) {
        const items = this.resultsList.children;
        this.activeIndex =
            (this.activeIndex + direction + items.length) % items.length;

        this.updateFocus();
    }

    select() {
        const items = this.resultsList.children;
        const index = this.activeIndex === -1 ? 0 : this.activeIndex;
        const li = items[index];
        if (!li) return;

        this.selectById(li.dataset.id);
    }

    selectById(id) {
        this.clearResults();
        this.activeIndex = -1;
        this.searchInput.value = "";
    
        const card = this.cardsContainer.querySelector(
            `article[data-id="${id}"]`
        );
        if (!card) return;
    
        this.clearSelectedCards();
        card.classList.add("selected");
    
        card.scrollIntoView({
            behavior: "smooth",
            block: "center"
        });

        const ids = [...this.cardsContainer.children].map(card => card.dataset.id)
        document.dispatchEvent(new CustomEvent("cardSelected", { detail: {id, ids} }))
    }    

    // Metodo per passare i dati al PanelController
    getData(id) {
        const champ = this.data[id];
        document.dispatchEvent(
            new CustomEvent("currentChamp", { detail: champ}))
    }

    // Sezione caricamento dinamico

    renderResults(query) {
        this.clearResults();

        for (const [id, champ] of Object.entries(this.data)) {
            if (!champ.name.toLowerCase().includes(query)) continue;

            const li = document.createElement("li");
            li.className = "result-item";
            li.dataset.id = id;
            li.innerHTML = `
                <div class="icon-champ-container">
                    <img src="${champ.icon}" loading="lazy" alt="${champ.name}">
                </div>
                <p>${champ.name} ~ <span>${champ.nickname}</span></p>
            `;

            li.addEventListener("mouseenter", () => {
                this.inputMode = "mouse";
                this.activeIndex = [...this.resultsList.children].indexOf(li);
                this.updateFocus();
            });
            
            this.resultsList.appendChild(li);
        }

        if (this.resultsList.children.length) {
            this.resultsBlock.classList.add("open");
            this.resultsBlock.scrollTop = 0;
        }
    }

    // Sezione UI

    updateFocus() {
        [...this.resultsList.children].forEach((item, i) => {
            item.classList.toggle("focus", i === this.activeIndex);
        });
        if (this.inputMode === "keyboard") {
            const activeItem = this.resultsList.children[this.activeIndex];
            activeItem?.scrollIntoView({
                block: "center",
                behavior: "smooth"
            });
        }
    }        

    clearResults() {
        this.resultsList.innerHTML = "";
        this.resultsBlock.classList.remove("open");
    }

    clearSelectedCards() {
        this.cardsContainer
            .querySelectorAll(".selected")
            .forEach(card => card.classList.remove("selected"));
    }
}
