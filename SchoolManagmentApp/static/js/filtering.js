// filtering

const filterButton = document.getElementById("filterButton");
const filterWindow = document.getElementById("filterWindow");
const filterButtonClose = document.getElementById("filterButtonClose");

filterButton.addEventListener("click", function () {
  filterWindow.style.display = "block";
});

filterButtonClose.addEventListener("click", function () {
  filterWindow.style.display = "none";
});
