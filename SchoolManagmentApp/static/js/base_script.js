var hamburger = document.querySelector(".hamb");
var navlist = document.querySelector(".nav-list");
var links = document.querySelector(".nav-list li");

hamburger.addEventListener("click", function () {
  this.classList.toggle("click");
  navlist.classList.toggle("open");
});

var typed = new Typed(".input", {
  strings: ["Private School.", "Student Support.", "Parents' Friends."],
  typeSpeed: 70,
  backSpeed: 60,
  loop: true,
});
