//inicializo la clase de las peticiones
const P = new Peticiones();

//obtener el script
const scriptElement = document.currentScript;

//obtengo los valores de data
const urlBuscarJuegos = scriptElement.getAttribute("data-urlbuscarjuegos");
const urlEmptyCard = scriptElement.getAttribute("data-empty-card");
const urlDetalleJuego = scriptElement
  .getAttribute("data-url-detalle")
  .replace("_slug_/", "");

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
              data-slug="${juego.slug}"
              class="btn btn-primary w-25 ver-juego"
              >Ver</a
            >
          </div>
        </div>
      </div>`;
}

function realizarBusqueda() {
  contenedorjuegos.textContent = ''
  contenedorjuegos.insertAdjacentHTML(
    "afterbegin",
    `<div class="card w-100 mb-2" aria-hidden="true">
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
      </div>`
  );
  espaciobutton.textContent = ''
  espaciobutton.insertAdjacentHTML(
    "afterbegin",
    `<div class="spinner-border spinner-border-sm" role="status">
            <span class="visually-hidden">Loading...</span>
          </div>`
  );
  //muestro el h2 y le quito el texto que tenga
  h2busqueda.classList.remove("hidden");
  h2busqueda.textContent = ``;
  espaciobutton.disabled = true;
  //hacer peticion
  //funcion cuando se realice la petición
  function petiReali(datos) {
    if (datos.juegos.length > 0) {
      h2busqueda.textContent = ''
      h2busqueda.insertAdjacentHTML(
        "afterbegin",
        `Resultados de la busqueda "${inputBusqueda.value.trim()}"`
      );

      contenedorjuegos.textContent = ``;
      datos.juegos.forEach((juego) => {
        contenedorjuegos.insertAdjacentHTML("beforeend",vistaJuego(juego))
      });
    } else if (datos.juegos.length < 1) {
      contenedorjuegos.textContent = ``;
      h2busqueda.textContent="Sin resultados"
    }
  }
  //funcion final (error o sin error)
  function final() {
    espaciobutton.textContent = ''
    espaciobutton.insertAdjacentHTML("afterbegin",`<i class="bi bi-search"></i>`)
    espaciobutton.disabled = false;
    eventoVerJuego();
  }
  P.peticionPost(
    urlBuscarJuegos,
    {
      busqueda: inputBusqueda.value.trim(),
      action: "busqueda",
    },
    petiReali,
    (funcionFinal = final)
  );
}

function cancelarBusqueda() {
  h2busqueda.classList.add("hidden");
  espaciobutton.textContent = ''
  espaciobutton.insertAdjacentHTML("afterbegin", `<i class="bi bi-search"></i>`)
  contenedorjuegos.textContent = ''
  contenedorjuegos.insertAdjacentHTML("afterbegin",valor_contenedorjuegos)
  eventoVerJuego();
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
              href="${urlDetalleJuego + juego.slug}"
              data-slug="${juego.slug}"
              class="btn btn-primary w-25 ver-juego"
              >Ver</a
            >
          </div>
        </div>
      </div>
  `;
}

function eventoVerJuego() {
  const a_ver = document.querySelectorAll(".ver-juego");
  const spn = F.spnCargando();
  a_ver.forEach((a) => {
    let url_juego = a.getAttribute("href");
    let slug_juego = a.getAttribute("data-slug");
    a.addEventListener("click", (e) => {
      e.preventDefault();
      a.appendChild(spn);
      //enviar peticion y en la funcion final enviarlo al detalle del juego
      P.peticionPost(
        ".",
        { juego: slug_juego },
        () => { },
        () => {
          a.removeChild(spn);
          window.location.href = url_juego;
        },
        (formdata = false)
      );
    });
  });
}

//ejecutar funciones
document.addEventListener("DOMContentLoaded", function (e) {
  eventoVerJuego();
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
      const spn = F.spnCargando(["align-self-center"]);
      h5_boton.appendChild(spn);
      boton.disabled = true;
      let slug = boton.getAttribute("data-slug").split("_")[2];
      //hacer peticion
      P.peticionPost(
        //url
        urlBuscarJuegos,
        //datos
        {
          action: "buscar_juego",
          slug: slug,
        },
        //funciona a realizar
        (data) => {
          // console.log(data);
          let juego = data.juego;
          let modal = new bootstrap.Modal(modalInfoJuego);
          modalTitle.textContent = juego.nombre;
          modalBody.textContent = "";
          modalBody.insertAdjacentHTML("afterbegin", plantillaModalBody(juego));
          eventoVerJuego();
          modal.show();
        },
        //funcion cuando se realice la peticion
        () => {
          // le pongo el valor al h5 y activo el boton
          h5_boton.removeChild(spn);
          boton.disabled = false;
        },
        //decir si es un formData
        (formdata = false)
      );
      //creo el objeto modal con bootstrap para poner mostrarlo y esconderlo y le paso el Nodo del div principal del modal
    });
  });
});
