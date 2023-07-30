var hamburger = document.querySelector('.hamb');
var navlist = document.querySelector('.nav-list');
var links = document.querySelector('.nav-list li');

hamburger.addEventListener('click', function(){
    this.classList.toggle('click');
    navlist.classList.toggle('open');
});


var typed = new Typed(".input", {
    strings:["Szkołą Prywatną.", "Wsparciem Ucznia.", "Przyjaciółmi Rodziców.", "5 LO w Zabrzu!"],
    typeSpeed: 70,
    backSpeed: 60,
    loop: true,
});

// commentSection 
const commentButtons = document.getElementById("login-nav-btn");
const commentSections = document.getElementsByClassName("login-form");

commentButtons.addEventListener("click", (event) => {
  console.log('click');
  event.preventDefault();
  commentSections[0].classList.toggle("login-form-hide");
});