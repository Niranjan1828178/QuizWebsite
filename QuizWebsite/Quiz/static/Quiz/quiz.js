
document.querySelector(".clear").addEventListener("click", ()=>{
    const radios = document.querySelectorAll('input[type="radio"]');
    radios.forEach(r => r.checked = false); 
  });

  