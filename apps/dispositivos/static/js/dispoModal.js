//obtener el script
const scriptElement = document.currentScript;

//obtengo los valores de data
const urlBuscarJuegosDispo = scriptElement.getAttribute(
  "data-url-buscar-juegos-dispo"
);

//acordeon
function acordeon(nombre, valores) {
  //funcion para crear cada acordeon, recibe nombre de la caracteristica y su arreglo de valores
  let ul = `<ul style="list-style-type: none;padding-left: 0;">`; //creo la ul para poner en el div seleccionado
  for (const diccionario of valores) {
    //recorro cada valor del diccionario con el for of (el for in me devolveria el indice)
    // utiliso el for of para el arreglo
    ul += `<hr>`; // pongo un hr en cada caracteristica
    for (const key in diccionario) {
      // recorro cada diccionario del arreglo
      // for in para cada diccionario
      if (diccionario.hasOwnProperty(key)) {
        const value = diccionario[key];
        if (key.includes("disponible_")) {
          let valor =
            "Disponible en patición " + key.split("_")[1].toUpperCase();
          ul += `<li><b>${valor}</b>: ${value}</li>`; // agrego los valores
        } else {
          ul += `<li><b>${valoresTextos[key]}</b>: ${value}</li>`; // agrego los valores
        }
      }
    }
  }
  //plantilla para los acordeones
  let acor = `<div class="accordion-item"> 
          <h2 class="accordion-header">
          <button
          class="accordion-button collapsed"
          type="button"
          data-bs-toggle="collapse"
          data-bs-target="#collapse${nombre.replace(/\s+/g, "")}"
          aria-expanded="false"
          aria-controls="collapseOne"
          >
           ${nombre}
          </button>
          </h2>
          <div
          id="collapse${nombre.replace(/\s+/g, "")}"
          class="accordion-collapse collapse"
          data-bs-parent="#carateristicas"
          >
          <div class="accordion-body">
          ${ul}
          </div>
          </div>
          </div>`;
  return acor; // retorno el acordeon creado
}

//activar - desactivar botones
function disabledBotones(botones) {
  botones.forEach((boton) => {
    boton.disabled = !boton.disabled;
  });
}

function dispoModal(
  botonesModalDispoQu,
  botonesEliminarDispoQu,
  modalDispoQu,
  modalTituloQu,
  modalBodyQu,
  btnSubmitQu,
  inputFormQu
) {
  const botonesModalDispo = document.querySelectorAll(botonesModalDispoQu);
  const botonesEliminarDispo = document.querySelectorAll(
    botonesEliminarDispoQu
  );
  const modalDispo = document.getElementById(modalDispoQu);
  const modalTitulo = modalDispo.querySelector(modalTituloQu);
  const modalBody = modalDispo.querySelector(modalBodyQu);
  const btnSubmit = document.getElementById(btnSubmitQu);
  const inputForm = document.getElementById(inputFormQu);

  botonesModalDispo.forEach((boton) => {
    //activar los botones
    boton.disabled = false;
    boton.addEventListener("click", function (e) {
      e.preventDefault();
      const divAcordeones = modalBody.querySelector("#carateristicas");
      //creo el spiner de bootstrap
      const spanLoading = spnCargando()
      boton.appendChild(spanLoading);
      disabledBotones(botonesModalDispo);
      let idDispo = 0;
      let clasesBoton = boton.className.split(" ");
      clasesBoton.forEach((element) => {
        if (element.includes("modalDispo")) {
          idDispo = element.replace("modalDispo", "");
        }
      });

      //con el id del dispositivo mando una petición con fetch para obtener la información del boton
      // Crea una nueva instancia del modal
      let modal = new bootstrap.Modal(modalDispo);
      //Aqui pongo los valores del dispositivo en el formulario
      //funcion de js/funciones.js
      peticionPost(
        window.location.pathname,
        { id: idDispo, action: "datosDispo" },
        (data) => {
          let dispo = data.dispositivo;
          modalTitulo.textContent = data.nombre;

          let acordeones = ``; //donde voy a crear el acordeon
          let keys = {
            rams: "Ram",
            discos: "Discos",
            sisOpe: "Sistema operativo",
            graficas: "Graficas",
            procesador: "Procesador",
          };
          for (const key in dispo) {
            // recorro los datos pasados por la peticion, con el for in para extraer el key, o clave
            if (dispo.hasOwnProperty(key)) {
              const value = dispo[key]; // obtengo el valor de esa clave
              acordeones += acordeon(keys[key], value); //le paso la clave y el valor a la funcion para crear el acordeon y luego sumarlo a los acordeones
            }
          }
          divAcordeones.textContent=''
          divAcordeones.insertAdjacentHTML("afterbegin",acordeones);
          modal.show();
        },
        () => {
          //quito el spinner del boton
          disabledBotones(botonesModalDispo);
          boton.removeChild(spanLoading);
        },
        //formdata
        false
      );
    });
  });
  botonesEliminarDispo.forEach((boton) => {
    //activar los botones
    boton.disabled = false;
    boton.addEventListener("click", function (e) {
      e.preventDefault();
      //deshabilitar el boton deL formulario e input
      btnSubmit.disabled = true;
      inputForm.disabled = true;

      //creo el spiner de bootstrap
      const spanLoading = spnCargando();
      boton.appendChild(spanLoading);
      disabledBotones(botonesEliminarDispo);
      let idDispo = 0;
      let clasesBoton = boton.className.split(" ");
      clasesBoton.forEach((element) => {
        if (element.includes("eliminarDispo")) {
          idDispo = element.replace("eliminarDispo", "");
        }
      });
      //funcion de js/funciones.js
      peticionPost(
        window.location.pathname,
        { id: idDispo, action: "eliminar" },
        (data) => {
          if (data.eliminacion) {
            const contenedor = document.querySelector(".contenedorDispo");
            const divDispo = contenedor.querySelector(`.dispoCont${idDispo}`);
            contenedor.removeChild(divDispo);
            let divDispoCount = contenedor.querySelectorAll(
              '[class*="dispoCont"]'
            ).length;
            if (divDispoCount == 0) {
              contenedor.textContent=''
              contenedor.insertAdjacentHTML(
                "afterbegin",
                "<h2>Sin dispositivos</h2>"
              );
            }
          }
        },
        () => {
          disabledBotones(botonesEliminarDispo);
          boton.removeChild(spanLoading);
          //activar formulario
          btnSubmit.disabled = false;
          inputForm.disabled = false;
        },
        //form data
        false
      );
    });
  });
}

function mostrarDispo(id, nombre, contenedor) {
  let plantilla = `
  <div class="w-auto mx-2 mb-3 dispoCont${id}">
    <div class="card">
      <div class="card-body">
        <h5 class="card-title">${nombre}</h5>
      </div>
      <div class="card-footer">
        <button class="btn btn-primary modalDispo${id}">
          Ver
        </button>
        <button class="btn btn-danger eliminarDispo${id}">
          Eliminar
        </button>
      </div>
    </div>
  </div>
  `;
  //preguntar cuantos dispositivos hay, si hay 0, limpio y agrego
  const dispositivos = contenedor.querySelectorAll('[class*="dispoCont"]');

  if (dispositivos.length == 0) {
    contenedor.textContent = ''
    contenedor.insertAdjacentHTML("afterbegin", plantilla);
  } else {
    contenedor.insertAdjacentHTML("beforeend", plantilla);
  }
}
