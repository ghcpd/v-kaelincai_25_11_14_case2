// Improved interactions to highlight hover, focus
const primaryButtons = document.querySelectorAll('.btn-primary')
primaryButtons.forEach(btn => {
  btn.addEventListener('click', () => {
    btn.textContent = 'Done ✓'
    btn.disabled = true
    btn.setAttribute('aria-pressed', 'true')
    btn.style.opacity = '0.8'
  })
})
