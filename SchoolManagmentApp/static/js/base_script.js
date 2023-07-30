
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


cancelButton.addEventListener("click", function () {
  hideDialog();
});


function proceedToDelete() {
  const deleteLink = document.getElementById("deleteEvent");
  const url = deleteLink.getAttribute("href");  
  window.location.href = url
}

function showDialog() {
  myDeleteConfirmer.classList.remove("hidden"); 
  myDeleteConfirmer.classList.add("animate__slideInDown");  
}

function hideDialog() {
    myDeleteConfirmer.classList.add("hidden");
}

// filtering

const filterButton = document.getElementById("filterButton");
const filterWindow = document.getElementById("filterWindow");
const filterButtonClose = document.getElementById("filterButtonClose");


filterButton.addEventListener("click", function() {
  filterWindow.style.display = "block";
});


filterButtonClose.addEventListener("click", function() {
  filterWindow.style.display = "none";
});