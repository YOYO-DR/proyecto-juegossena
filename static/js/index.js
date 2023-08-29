
document.addEventListener("DOMContentLoaded", function (e) {
  //seleccionar elementos
  const inputBusqueda = document.getElementById("inputBusqueda");
  inputBusqueda.addEventListener("input", function (e) { 
    if (inputBusqueda.value.trim() !== "") { console.log(inputBusqueda.value); }
  })
})