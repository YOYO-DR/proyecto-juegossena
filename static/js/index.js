//obtener el script
const scriptElement = document.currentScript;

//obtengo los valores de data
const urlBuscarJuegos = scriptElement.getAttribute("data-urlbuscarjuegos");
const urlEmptyCard = scriptElement.getAttribute("data-empty-card");

//constantes
const h2busqueda = document.querySelector(".h2-busqueda");
const inputBusqueda = document.getElementById("inputBusqueda");
const contenedorjuegos = document.querySelector(".contenedor-juegos");
const espaciobutton = document.querySelector(".espacio-button");
const valor_contenedorjuegos = contenedorjuegos.innerHTML;

//funciones
//crear vista de juego
function vistaJuego(juego) {
  return `<div class="card w-100 mb-2" id="juego_${juego.id}">
        <img
          src="${juego.imagen}"
          class="card-img-top img-juego mx-auto m-1"
          alt="${juego.nombre}"
        />
        <div class="card-body">
          <div class="d-flex justify-content-center align-item-center">
            <h5 class="card-title me-3 fs-4">${juego.nombre}</h5>
            <button
              class="btn-hidden"
              data-toggle="tooltip"
              data-placement="top"
              title="Agregar a favoritos"
            >
              <i class="fs-4 bi-heart"></i>
            </button>
          </div>
          <p class="card-text">
            ${juego.descripcion}
          </p>
          <a href="#${juego.id}" class="btn btn-primary">Ver</a>
        </div>
      </div>`;
}
function realizarBusqueda() {
  contenedorjuegos.innerHTML = `<div class="card w-100 mb-2" aria-hidden="true">
        <img
          src="${urlEmptyCard}"
          class="card-img-top card-img-top img-juego mx-auto m-1"
          alt="..."
        />
        <div class="card-body">
          <h5 class="card-title placeholder-glow">
            <span class="placeholder col-6"></span>
          </h5>
          <p class="card-text placeholder-glow">
            <span class="placeholder col-7"></span>
            <span class="placeholder col-4"></span>
            <span class="placeholder col-4"></span>
            <span class="placeholder col-6"></span>
            <span class="placeholder col-8"></span>
          </p>
          <a
            class="btn btn-primary disabled placeholder col-5 col-sm-2"
            aria-disabled="true"
          ></a>
        </div>
      </div>`;
  h2busqueda.innerHTML = `Resultados de la busqueda "${inputBusqueda.value.trim()}"`;
  h2busqueda.classList.remove("hidden");
  espaciobutton.innerHTML = `<div class="spinner-border spinner-border-sm" role="status">
            <span class="visually-hidden">Loading...</span>
          </div>`;
  espaciobutton.disabled = true;
  //hacer peticion
  //funcion cuando se realice la petición
  function petiReali(datos) {
    if (!("error" in datos)) {
      contenedorjuegos.innerHTML = ``;
      datos.juegos.forEach((juego) => {
        contenedorjuegos.innerHTML += vistaJuego(juego);
      });
    } else {
      alert("Error: "+datos.error)
    }
  }
  //funcion final (error o sin error)
  function final() {
    espaciobutton.innerHTML = `<i class="bi bi-search"></i>`;
    espaciobutton.disabled = false;
  }
  peticionPost(urlBuscarJuegos, { busqueda: inputBusqueda.value.trim() }, petiReali, (funcionFinal = final));
  
  //prueba para que se vea el boton cargando
}
function cancelarBusqueda() {
  h2busqueda.classList.add("hidden");
  espaciobutton.innerHTML = `<i class="bi bi-search"></i>`;
  contenedorjuegos.innerHTML = valor_contenedorjuegos;
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
      cancelarBusqueda();
    }
  });
});
