// Minimal interactions to support the demo
document.querySelectorAll('.btn-primary').forEach(btn=>btn.addEventListener('click',e=>{
  btn.textContent='Done ✓';
  btn.disabled=true;
  btn.style.opacity='0.7';
}));
