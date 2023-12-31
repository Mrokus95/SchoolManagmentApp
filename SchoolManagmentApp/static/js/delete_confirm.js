const myDeleteConfirmer = document.getElementById("myDeleteConfirmer");
const confirmButton = document.getElementById("deleteConfirmButton");
const cancelButton = document.getElementById("deleteCancelButton");
const deleteButton = document.getElementById("deleteEvent");

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

