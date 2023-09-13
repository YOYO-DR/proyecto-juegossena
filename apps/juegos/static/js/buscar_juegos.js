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

//realizar busqueda
function buscar(input, radios, check = null,buscar=null) {
  //(check,radios,input)
  //check=id del checkbox del evento
  //radios = [lista y pregunto cual es el precionado ya que solo seria 1]
  //input = div.input-group de la busqueda > input y button{i del icono}

  const ckeckboxs = document.querySelectorAll(`input[type="checkbox"]`);
  const juegosDiv = document.querySelector(".juegos-muestra");

  //ejecuto la busqueda solo si el input tiene datos
  if (input.value.trim()) {
    //constantes
    const btnInputBuscar = document.querySelector(".espacio-button");
    const spnCargar = spnCargando();

    //datos a enviar
    let datosEnvio = {busqueda:input.value};

    //buscar
    //desactivar
    //desactivar input
    input.disabled = true;
    //desactivar boton del input
    btnInputBuscar.disabled = true;
    //quitar el i del boton solo si se hace la peticion por el enter del input o click del boton y poner el spinner
    if (buscar) {
      //se lo quito y le pongo el spinner
      btnInputBuscar.innerHTML = '';
      btnInputBuscar.appendChild(spnCargar)
    }
    //inicializar el campo de checkbox para enviar
    datosEnvio.checkbox = [];
    ckeckboxs.forEach((checkbox) => {
      if (check) {
        if (checkbox.getAttribute("id") == check) {
          //le agrego el spinner
          document
            .querySelector(`label[for="${checkbox.getAttribute("id")}"]`)
            .appendChild(spnCargar);
        }
      }
      datosEnvio.checkbox.push({
        value: checkbox.value,
        checked: checkbox.checked,
      });
      checkbox.disabled = true;
    });
    //desactivar radios y ponerle el spn al radio seleccionado
    radios.forEach((radio) => {
      radio.disabled = true;
      //no le pongo el spinner porque el del evento fue un checkbox y poer eso llego el parametro check
      if (radio.checked) {
        //le pone el radio solo si el check no existe ni la busqueda, por lo cual el del evento debe ser un radio
        if (!check && !buscar) {
          //obtengo el label del radio
          const label = document.querySelector(
            `label[for="${radio.getAttribute("id")}"]`
          );
          label.appendChild(spnCargar);
        }
        datosEnvio.dispo = { id: radio.getAttribute("id") };
      }
    });

    //datos a enviar
    //datosEnvio
    //hacer peticion
    peticionPost(
      //url
      ".",
      //datos
      datosEnvio,
      //funcion
      function callback(datos) {
        console.log(datos);
        let juegos = datos.juegos
        if (juegos.length > 0) {
          let ul = `<ul>`;
          juegos.forEach((juego) => {
            ul += `<li><a href="${urlDetalleJuego}${juego.slug}">${juego.nombre}</a></li>`;
          });
          juegosDiv.innerHTML = ul + `</ul>`;
        } else {
          juegosDiv.innerHTML=`<h2>Sin resultados</h2>`
        }
      },
      () => {
        //activar checkboxs
        ckeckboxs.forEach((checkbox) => {
          if (check) {
            if (checkbox.getAttribute("id") == check) {
              document
                .querySelector(`label[for="${checkbox.getAttribute("id")}"]`)
                .removeChild(spnCargar);
            }
          }
          checkbox.disabled = false;
        });
        //activar input
        input.disabled = false;
        //activar boton del input
        btnInputBuscar.disabled = false;
        //quitar spinner y poner el i del boton de nuevo
        if (buscar) {
          //lo limpio quitando el spinner y ponerle el i del icono
          btnInputBuscar.innerHTML=`<i class="bi bi-search"></i>`
        }
        //activar radios
        radios.forEach((radio) => {
          radio.disabled = false;
          if (radio.checked) {
              if (!check && !buscar) {
                //obtengo el label del radio
                const label = document.querySelector(
                  `label[for="${radio.getAttribute("id")}"]`
                );
                label.removeChild(spnCargar);
              }
          }
        });
      },
      (formdata = false)
    );
  } else {
    mensajeSweet("Debe ingresar un valor en la busqueda", "warning");
  }
}

//busqueda input o boton de busqueda
function busquedaInputButtom(input,radios) {
  buscar(input, radios, (check = null), (busqueda = true));
}

document.addEventListener("DOMContentLoaded", (e) => {
  //constantes
  const radioInputs = document.querySelectorAll('input[name="dispo');
  const opciones = document.querySelector(".opciones");
  const botonOpciones = opciones.querySelector("button");
  const checkboxs = document.querySelectorAll(
    `.form-check input[type="checkbox"]`
  );
  const inputBuscar = document.querySelector("#inputBusqueda");
  const botonBusqueda = document.querySelector(".espacio-button");
  let sumaCheckbox = heightCheckbox(opciones.querySelectorAll(".form-check"));

  //evento de los checkboxs
  checkboxs.forEach((checkbox) => {
    checkbox.addEventListener("click", (e) => {
      if (!inputBuscar.value.trim()) {
        //si el input etsa vacio, no dejo que lo marque
        checkbox.checked = !checkbox.checked;
      }
      buscar(inputBuscar, radioInputs, checkbox.getAttribute("id"));
    });
  });

  //evento de cuando se seleccione un radio
  radioInputs.forEach((radio) => {
    radio.addEventListener("click", (e) => {
      //ejecuto el buscar
      // Evita que se marque el radio button si el campo de búsqueda está vacío
      if (!inputBuscar.value.trim()) {
        e.preventDefault();
      }
      //de igual forma se ejecuta porque ahi tengo la notificacion de verificacion
      buscar(inputBuscar, radioInputs);
    });
  });

  //evento del boton buscar o enter en el input

  //buscar(input, radios, check = null,busqueda=null)
  inputBuscar.addEventListener("keydown", (e) => {
    if (e.key === "Enter") {
      busquedaInputButtom(inputBuscar,radioInputs);
    }
  })
  botonBusqueda.addEventListener("click", (e) => { 
    e.preventDefault()
    busquedaInputButtom(inputBuscar, radioInputs);
  })
  
  let botonOpcionesHeight = botonOpciones.offsetHeight; // obtén la altura del botón
  opciones.style.maxHeight = `${botonOpcionesHeight}px`;
  //boton de las opciones
  botonOpciones.addEventListener("click", (e) => {
    if (opciones.classList.contains("activa")) {
      opciones.style.maxHeight = `${botonOpcionesHeight}px`; // establece la altura máxima al tamaño del botón
    } else {
      opciones.style.maxHeight = sumaCheckbox + sumaCheckbox * 0.4 + "px"; //sumo el tamaño de cada checkbox mas un 40%
    }
    opciones.classList.toggle("activa");
  });
});
