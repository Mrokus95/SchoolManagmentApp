function toggleTextVisibility(event) {
    const iconElement = event.target;
    const textElement = iconElement.parentElement.nextElementSibling;
    textElement.classList.toggle('visible');
  }

  const icons = document.querySelectorAll('.cards button i');

  icons.forEach(icon => {
    icon.addEventListener('click', toggleTextVisibility);
  });