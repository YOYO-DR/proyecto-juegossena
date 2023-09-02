//obtener el script
const scriptElement = document.currentScript;

//obtengo los valores de data
const urlBuscarJuegos = scriptElement.getAttribute("data-urlbuscarjuegos");
const urlEmptyCard = scriptElement.getAttribute("data-empty-card");
const urlDetalleJuego = scriptElement
  .getAttribute("data-url-detalle")
  .replace("_slug_", "");


//constantes
const h2busqueda = document.querySelector(".h2-busqueda");
const inputBusqueda = document.getElementById("inputBusqueda");
const contenedorjuegos = document.querySelector(".contenedor-juegos");
const espaciobutton = document.querySelector(".espacio-button");
const valor_contenedorjuegos = contenedorjuegos.innerHTML;
const botonesJuegosMasB = document.querySelectorAll(
  'button[data-slug*="id_juego_"]'
);
//elementos del modal
const modalInfoJuego = document.getElementById("modal-info-juego");
const modalTitle = modalInfoJuego.querySelector(".modal-title");
const modalBody = modalInfoJuego.querySelector(".modal-body");
//spinner
const spnCargando = `<div class="ms-1 spinner-border spinner-border-sm align-self-center" role="status">
<span class="visually-hidden">Loading...</span>
</div>`;

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

          <div class="d-flex flex-column align-items-center">
            <a href="${juego.urlPagina}" class="link mb-2" target="_blank"
              >Página oficial</a
            >
            <a
              href="${urlDetalleJuego + juego.slug}"
              class="btn btn-primary w-25"
              >Ver</a
            >
          </div>
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
  espaciobutton.innerHTML = `<div class="spinner-border spinner-border-sm" role="status">
            <span class="visually-hidden">Loading...</span>
          </div>`;
  //muestro el h2 y le quito el texto que tenga
  h2busqueda.classList.remove("hidden");
  h2busqueda.innerHTML=''
  espaciobutton.disabled = true;
  //hacer peticion
  //funcion cuando se realice la petición
  function petiReali(datos) {
    if (!("error" in datos) && datos.juegos.length > 0) {
      
      h2busqueda.innerHTML = `Resultados de la busqueda "${inputBusqueda.value.trim()}"`;
      

      contenedorjuegos.innerHTML = ``;
      datos.juegos.forEach((juego) => {
        contenedorjuegos.innerHTML += vistaJuego(juego);
      });
    } else if (datos.juegos.length < 1) {
      contenedorjuegos.innerHTML = ``;
      h2busqueda.innerHTML="Sin resultados";
    } else {
      alert("Error: " + datos.error);
    }
  }
  //funcion final (error o sin error)
  function final() {
    espaciobutton.innerHTML = `<i class="bi bi-search"></i>`;
    espaciobutton.disabled = false;
  }
  peticionPost(
    urlBuscarJuegos,
    {
      busqueda: inputBusqueda.value.trim(),
      action: "busqueda"
    },
    petiReali,
    (funcionFinal = final)
  );

  //prueba para que se vea el boton cargando
}
function cancelarBusqueda() {
  h2busqueda.classList.add("hidden");
  espaciobutton.innerHTML = `<i class="bi bi-search"></i>`;
  contenedorjuegos.innerHTML = valor_contenedorjuegos;
}
function plantillaModalBody(juego) {
  return `
  <div class="card" id="juego_{{juego.id}}">
        <img
          src="${juego.imagen}"
          class="card-img-top img-juego mx-auto m-1"
          alt="${juego.nombre}"
        />
        <div class="card-body">
          <div class="d-flex flex-column align-items-center">
            <a href="${juego.urlPagina}" class="link mb-2" target="_blank"
              >Página oficial</a
            >
            <a
              href="${urlDetalleJuego+juego.slug}"
              class="btn btn-primary w-25"
              >Ver</a
            >
          </div>
        </div>
      </div>
  `;
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
  //evento click a los botones de los juegos más buscados
  botonesJuegosMasB.forEach(function (boton) {
    boton.addEventListener("click", function (e) {
      e.preventDefault();
      const h5_boton = boton.querySelector("h5");
      let valorh5 = h5_boton.innerHTML;
      h5_boton.innerHTML += spnCargando;
      boton.disabled = true;
      let slug = boton.getAttribute("data-slug").split("_")[2];
      //hacer peticion
      peticionPost(
        //url
        urlBuscarJuegos,
        //datos
        {
          action: "buscar_juego",
          slug: slug,
        },
        //funciona a realizar
        (data) => {
          if (!("error" in data)) {
            console.log(data);
            let juego=data.juego
            let modal = new bootstrap.Modal(modalInfoJuego);
            modalTitle.innerHTML = juego.nombre;
            modalBody.innerHTML = plantillaModalBody(juego);
            modal.show();
          } else {
            console.error("Error: "+ data.error)
          }
        },
        //funcion cuando se realice la peticion
        () => {
          // le pongo el valor al h5 y activo el boton
          h5_boton.innerHTML = valorh5;
          boton.disabled = false;
        },
        //decir si es un formData
        (formdata = false)
      );
      //creo el objeto modal con bootstrap para poner mostrarlo y esconderlo y le paso el Nodo del div principal del modal
      
      
      
    });
  });
});
