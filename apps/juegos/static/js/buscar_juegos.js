//funciones
//obtener script y obtener la url del detalle juego
const urlDetalleJuego = document.currentScript
  .getAttribute("data-url-detalle-juego")
  .replace("_slug_/", "");

//height de cada checkbox
function heightCheckbox(checkbox) {
  let sumaHeight = 0;
  checkbox.forEach((check) => {
    sumaHeight += check.offsetHeight;
  });
  return sumaHeight;
}

//Plantilla de la busqueda
function plantillaBusqueda(dispositivo, juego, comparacion) {
  let suma_rams_dispo = 0;
  for (let i = 0; i < dispositivo.rams.length; i++) {
    suma_rams_dispo += parseFloat(
      dispositivo.rams[i].tamano.replace(" GB", "")
    );
  }
  let plantilla = `
    <div class="border rounded p-2 m-2 d-flex flex-column flex-md-row juego_${
      juego.id
    }">
      <div
        class="col-12 col-md-6 p-2 d-flex flex-column align-items-center justify-content-center"
      >
        <img
          class="img-fluid rounded"
          src="${juego.imagen}"
          alt="Imagen de ${juego.nombre}"
        />
        <a href="/juegos/detalle/${juego.slug}/" class="fs-4 mt-2 text-center"
          >${juego.nombre}</a
        >
      </div>
      <div class="col-12 col-md-6 p-2 d-flex flex-column">
        <div class="d-flex flex-column border p-2 my-1 ${
          comparacion.procesador ? "bg-compatible" : "bg-incompatible"
        }">
          <h5><b>Procesador</b></h5>
          <span><b>Juego:</b> ${juego.procesador.nombre}</span>
          <span
            ><b>Dispositivo:</b> ${dispositivo.procesador[0].modelo}</span
          >
        </div>
        <div class="d-flex flex-column border p-2 my-1 ${
          comparacion.ram ? "bg-compatible" : "bg-incompatible"
        }">
          <h5><b>Ram</b></h5>
          <span><b>Juego:</b> ${juego.ram.gb} GB</span>
          <span><b>Dispositivo:</b> ${suma_rams_dispo} GB</span>
        </div>
        <div class="d-flex flex-column border p-2 my-1 ${
          comparacion.grafica[0] ? "bg-compatible" : "bg-incompatible"
        }">
          <h5><b>Gráfica</b></h5>
          <span><b>Juego:</b> ${juego.grafica.nombre}</span>
          <span><b>Dispositivo:</b> ${comparacion.grafica[1]}</span>
        </div>
        <div class="d-flex flex-column border p-2 my-1 ${
          comparacion.disco[0] ? "bg-compatible" : "bg-incompatible"
        }">
          <h5><b>Espacio requerido</b></h5>
          <span><b>Juego:</b> ${juego.espacio} GB</span>
          <span><b>Dispositivo:</b> (${toTitle(comparacion.disco[1][0])}) ${
    comparacion.disco[1][1]
  } GB </span>
        </div>
      </div>
    </div>`;
  return plantilla;
}

//realizar busqueda
function buscar(input, radios) {
  const checkboxs = document.querySelectorAll(`input[type="checkbox"]`);
  const juegosDiv = document.querySelector(".juegos-muestra");
  const check_buscar = document.querySelector("#requi");

  //ejecuto la busqueda solo si el input tiene datos
  if (input.value.trim()) {
    //constantes
    const btnInputBuscar = document.querySelector(".espacio-button");
    const spnCargar = spnCargando();

    //datos a enviar
    let datosEnvio = { busqueda: input.value };

    //buscar
    //desactivar
    //desactivar input
    input.disabled = true;
    //desactivar boton del input
    btnInputBuscar.disabled = true;
    //quitar el i del boton solo si se hace la peticion por el enter del input o click del boton y poner el spinner
      btnInputBuscar.textContent = ``;
      btnInputBuscar.appendChild(spnCargar);
    
    //inicializar el campo de checkbox para enviar
    datosEnvio.checkbox = [];
    checkboxs.forEach((checkbox) => {
      datosEnvio.checkbox.push({
        value: checkbox.value,
        checked: checkbox.checked,
      });
    });
    //desactivar radios y ponerle el spn al radio seleccionado
    radios.forEach((radio) => {
      // verifico que radio esta checkeado y obtengo el id del dispositivo
      if (radio.checked) {
        datosEnvio.dispo = { id: radio.getAttribute("id") };
      }
    });

    //pongo la pantalla de carga
    juegosDiv.textContent = ''
    juegosDiv.insertAdjacentHTML(
      "afterbegin",
      `<div class="border rounded p-2 m-2 d-flex flex-column flex-md-row juego_0">
      <div
        class="col-12 col-md-6 p-2 d-flex flex-column align-items-center justify-content-center"
      >
        <img
          class="img-fluid rounded"
          src="https://djangoyoiner.blob.core.windows.net/juegossena/static/media/img/empty-card.jpg"
          alt="Imagen de carga"
        />
        <h5 class="placeholder-glow w-100">
          <span class="placeholder col-12"></span>
        </h5>
      </div>
      <div class="col-12 col-md-6 p-2 d-flex flex-column">
        <!--procesador-->
        <div class="d-flex flex-column border p-2 my-1">
        <!--Titulo procesador-->
          <span class="placeholder-glow"><span class="placeholder col-6"></span></span>
        <!--juego-->
          <span class="placeholder-glow"><span class="placeholder col-11"></span></span>

          <!--dispositivo y valor-->
          <span class="placeholder-glow"><span class="placeholder col-5"></span></span>
          <span class="placeholder-glow"><span class="placeholder col-11"></span></span>

        </div>

        <!--ram-->
        <div class="d-flex flex-column border p-2 my-1">
        <!--Titulo ram-->
          <span class="placeholder-glow"><span class="placeholder col-3"></span></span>
        <!--juego-->
          <span class="placeholder-glow"><span class="placeholder col-3"></span></span>

          <!--dispositivo-->
          <span class="placeholder-glow"><span class="placeholder col-5"></span></span>
        </div>

        <!--grafica-->
        <div class="d-flex flex-column border p-2 my-1">
        <!--Titulo grafica-->
          <span class="placeholder-glow"><span class="placeholder col-4"></span></span>
        <!--juego-->
          <span class="placeholder-glow"><span class="placeholder col-3"></span></span>

          <!--dispositivo y valor-->
          <span class="placeholder-glow"><span class="placeholder col-5"></span></span>
          
          <span class="placeholder-glow"><span class="placeholder col-11"></span></span>
        </div>
        
        <!--espacio requerido-->
        <div class="d-flex flex-column border p-2 my-1">
        <!--Titulo espacio requerido-->
          <span class="placeholder-glow"><span class="placeholder col-8"></span></span>
        <!--juego-->
          <span class="placeholder-glow"><span class="placeholder col-3"></span></span>

          <!--dispositivo-->
          <span class="placeholder-glow"><span class="placeholder col-5"></span></span>
        </div>
      </div>`
    );

    //datos a enviar
    //datosEnvio
    //hacer peticion
    console.log(datosEnvio)
    peticionPost(
      //url
      ".",
      //datos
      datosEnvio,
      //funcion
      function callback(datos) {
        let juegos = datos.juegos;
        let dispositivo = datos.dispo;
        if (juegos.length > 0) {
          let juegosLista = ``;
          for (let i = 0; i < juegos.length; i++) {
            juegosLista += plantillaBusqueda(
              dispositivo,
              juegos[i].juego,
              juegos[i].comparacion
            );
          }
          juegosDiv.textContent = ''
          juegosDiv.insertAdjacentHTML("afterbegin", juegosLista);
        } else {
          juegosDiv.textContent = "";
          juegosDiv.insertAdjacentHTML("afterbegin",  `<h2 class="w-100 text-center mt-3">Sin resultados</h2>`);
        }
      },
      () => {
        //activar input
        input.disabled = false;
        //activar boton del input
        btnInputBuscar.disabled = false;
        //lo limpio quitando el spinner y ponerle el i del icono
        btnInputBuscar.textContent = ''
        btnInputBuscar.insertAdjacentHTML("afterbegin",`<i class="bi bi-search"></i>`)
      },
      (formdata = false)
    );
  } else {
    mensajeSweet("Debe ingresar un valor en la busqueda", "warning");
  }
}

//busqueda input o boton de busqueda
function busquedaInputButtom(input, radios) {
  buscar(input, radios);
}

document.addEventListener("DOMContentLoaded", (e) => {
  //constantes
  const radioInputs = document.querySelectorAll('input[name="dispo');
  const opciones = document.querySelector(".opciones");
  const botonOpciones = opciones.querySelector("button");
  const checkboxs = document.querySelectorAll(
    `.form-check input[type="checkbox"]`
  );
  const check_requi = document.querySelector(
    `#requi`
  );
  const inputBuscar = document.querySelector("#inputBusqueda");
  const botonBusqueda = document.querySelector(".espacio-button");

  let sumaCheckbox = heightCheckbox(opciones.querySelectorAll(".form-check"));

  //evento del check "buscar con requisitos"
  check_requi.addEventListener("click", (e) => {
    if (check_requi.checked) {
      checkboxs.forEach((check) => {
        if (check.getAttribute("id") !== "requi") {
          check.disabled = false;
        }
      });
    } else {
      checkboxs.forEach((check) => {
        if (check.getAttribute("id") !== "requi") {
          check.disabled = true;
        }
      });
    }
    
  });


  //evento del boton buscar o enter en el input

  //buscar(input, radios, check = null,busqueda=null)
  inputBuscar.addEventListener("keydown", (e) => {
    if (e.key === "Enter") {
      busquedaInputButtom(inputBuscar, radioInputs);
    }
  });
  botonBusqueda.addEventListener("click", (e) => {
    e.preventDefault();
    busquedaInputButtom(inputBuscar, radioInputs);
  });

  let botonOpcionesHeight = botonOpciones.offsetHeight; // obtén la altura del botón
  opciones.style.maxHeight = `${botonOpcionesHeight}px`;
  //boton de las opciones. tamaño para que se adapte en desarrollo y producción
  botonOpciones.addEventListener("click", (e) => {
    if (opciones.classList.contains("activa")) {
      opciones.style.maxHeight = `${botonOpcionesHeight}px`; // establece la altura máxima al tamaño del botón
    } else {
      opciones.style.maxHeight = `${sumaCheckbox + sumaCheckbox * 0.4}px`; //sumo el tamaño de cada checkbox mas un 40%
    }
    opciones.classList.toggle("activa");
  });
});
