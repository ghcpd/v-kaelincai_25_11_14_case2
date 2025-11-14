// Improved UI behavior: hover states and keyboard focus with accessible outlines
const primaries=document.querySelectorAll('.task-card .btn-primary');
primaries.forEach(btn=>{
  btn.addEventListener('mouseover',()=>btn.style.boxShadow='rgba(13,71,161,0.18) 0px 6px 18px');
  btn.addEventListener('mouseout',()=>btn.style.boxShadow='');
  btn.addEventListener('focus',()=>btn.style.boxShadow='rgba(13,71,161,0.18) 0px 6px 18px');
  btn.addEventListener('blur',()=>btn.style.boxShadow='');
});
