//  variables
const filterButton = document.getElementById("filterButton");
const filterWindow = document.getElementById("filterWindow");
const filterButtonClose = document.getElementById("filterButtonClose");
const myDeleteConfirmer = document.getElementById("myDeleteConfirmer");
const confirmButton = document.getElementById("deleteConfirmButton");
const cancelButton = document.getElementById("deleteCancelButton");
const deleteButton = document.getElementById("deleteEvent");



// deleter siplay
myDeleteConfirmer.classList.add("hidden");

deleteButton.addEventListener("click", function (event) {
  event.preventDefault();
});

confirmButton.addEventListener('click', function() {
    hideDialog();
    proceedToDelete();
});

// schowanie okna potwierdzenia w przypadku kliknięcia anuluj
cancelButton.addEventListener("click", function () {
  hideDialog();
});

// funkcja do wyjebania zasobu
function proceedToDelete() {
  const deleteLink = document.getElementById("deleteEvent");
  const url = deleteLink.getAttribute("href");  // Pobranie adresu URL z atrybutu "href"
  window.location.href = url
}

function showDialog() {
  myDeleteConfirmer.classList.remove("hidden"); 
  myDeleteConfirmer.classList.add("animate__slideInDown");  
}

function hideDialog() {
  myDeleteConfirmer.classList.add("animate__slideOutUp");
  myDeleteConfirmer.addEventListener("animationend", function () {
    myDeleteConfirmer.classList.add("hidden");
    myDeleteConfirmer.classList.remove("animate__slideOutUp");
  });
}
