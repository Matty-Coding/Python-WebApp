const body = document.querySelector("body");
const darkIcon = document.querySelector("#dark-icon");
const lightIcon = document.querySelector("#light-icon");

const darkFilled = "bi-moon-fill";
const darkUnfilled = "bi-moon";
const lightUnfilled = "bi-sun";
const lightFilled = "bi-sun-fill";

const themeToggle = document.querySelector(".theme-toggle");

const themeMeta = document.querySelector("#theme-meta");

themeToggle.addEventListener("click", (e) => {
    if (e.target === darkIcon) {
        body.classList.replace("light-theme", "dark-theme");
        darkIcon.classList.replace(darkUnfilled, darkFilled);
        lightIcon.classList.replace(lightFilled, lightUnfilled);
        lightIcon.classList.remove("current-theme");
        darkIcon.classList.add("current-theme");
        
        const currentTheme = document.querySelector(".current-theme");
        currentTheme.style.borderBottom = "wheat 2px solid";

        themeMeta.setAttribute("content", "#151515");

    } else {
        body.classList.replace("dark-theme", "light-theme");
        darkIcon.classList.replace(darkFilled, darkUnfilled);
        lightIcon.classList.replace(lightUnfilled, lightFilled);
        darkIcon.classList.remove("current-theme");
        lightIcon.classList.add("current-theme");
        
        const currentTheme = document.querySelector(".current-theme");
        currentTheme.style.borderBottom = "#151515 2px solid";
            
        themeMeta.setAttribute("content", "#f5deb3");
    }
});