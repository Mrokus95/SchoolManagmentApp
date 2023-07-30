var hamburger = document.querySelector('.hamb');
var navlist = document.querySelector('.nav-list');
var links = document.querySelector('.nav-list li');

hamburger.addEventListener('click', function(){
    this.classList.toggle('click');
    navlist.classList.toggle('open');
});



// Pobieramy elementy z DOM
const filterButton = document.getElementById("filterButton");
const filterWindow = document.getElementById("filterWindow");
const filterButtonClose = document.getElementById("filterButtonClose");



// Dodajemy obsługę kliknięcia guzika
filterButton.addEventListener("click", function() {
    filterWindow.style.display = "block";
});

// Dodajemy obsługę kliknięcia przycisku zamykania
filterButtonClose.addEventListener("click", function() {
    filterWindow.style.display = "none";
});

