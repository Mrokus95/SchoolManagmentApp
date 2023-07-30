// replySection 
const replyButton = document.getElementById("reply_button");
const replySection = document.getElementById("reply-section");

replyButton.addEventListener("click", (event) => {
  console.log('click');
  event.preventDefault();
  replySection.classList.toggle("hide-section");
});
