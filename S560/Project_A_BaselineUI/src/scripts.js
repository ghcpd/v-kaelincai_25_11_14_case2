// Minimal behavior: hover & focusing buttons show inconsistent results
document.querySelectorAll('.task-card .btn-primary').forEach(btn => {
  btn.addEventListener('mouseover', () => {
    // baseline: some buttons change color inconsistently
    if(btn.classList.contains('green')) btn.style.background = '#2e7d32';
    else if(btn.classList.contains('red')) btn.style.background = '#d32f2f';
    else btn.style.opacity = '0.95';
  });
  btn.addEventListener('mouseout', () => {
    if(btn.classList.contains('green')) btn.style.background = 'green';
    else if(btn.classList.contains('red')) btn.style.background = '#b71c1c';
    else btn.style.opacity = '';
  });
});
