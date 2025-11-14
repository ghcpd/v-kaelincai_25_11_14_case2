const cards = document.querySelectorAll('.improved-card');
cards.forEach(card => {
  card.addEventListener('focus', () => card.classList.add('focused'));
  card.addEventListener('blur', () => card.classList.remove('focused'));
});
