const cards = document.querySelectorAll('.task-card');
cards.forEach(card => {
  card.addEventListener('mouseenter', () => {
    card.style.borderColor = '#999';
  });
  card.addEventListener('mouseleave', () => {
    card.style.borderColor = '#c7c7c7';
  });
});
