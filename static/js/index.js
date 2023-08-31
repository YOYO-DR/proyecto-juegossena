//constantes
const h2busqueda = document.querySelector(".h2-busqueda");
const inputBusqueda = document.getElementById("inputBusqueda");
const contenedorjuegos = document.querySelector(".contenedor-juegos");
const espaciobutton = document.querySelector(".espacio-button");
//funciones
function realizarBusqueda() {
  h2busqueda.innerHTML = `Resultados de la busqueda "${inputBusqueda.value.trim()}"`;
  h2busqueda.classList.remove("hidden");
  espaciobutton.innerHTML = `<div class="spinner-border spinner-border-sm" role="status">
            <span class="visually-hidden">Loading...</span>
          </div>`;
  setTimeout(function () {
    espaciobutton.innerHTML = `<i class="bi bi-search"></i>`;
  }, 1000);
}
function cancelarBusqueda() {
  h2busqueda.classList.add("hidden");
  espaciobutton.innerHTML = `<i class="bi bi-search"></i>`;
}

//ejecutar funciones
document.addEventListener("DOMContentLoaded", function (e) {
  //cuando le unda click al boton
  espaciobutton.addEventListener("click", function (e) {
    e.preventDefault();
    realizarBusqueda();
  });

  //cuando le de enter dentro del input
  inputBusqueda.addEventListener("keydown", function (e) {
    if (e.key === "Enter") {
      realizarBusqueda();
    }
  });

  //cancelar busqueda si el input queda vacio
  inputBusqueda.addEventListener("input", function (e) {
    if (inputBusqueda.value === "") {
      cancelarBusqueda()
    }
  });
});
