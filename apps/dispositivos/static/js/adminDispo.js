//Inicializo la clase de peticiones
const P = new Peticiones();

//obtener el script
const scriptElement = document.currentScript;

//obtengo los valores de data
const urlProcesarDispo = scriptElement.getAttribute("data-url-procesar-dispo");

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
//activar elementos con atributo disabled
function activarElementosDisabled(elementos) {
  elementos.forEach((elemento) => {
    elemento.disabled = false;
  })
}

//desactivar elementos con atributo disabled
function desactivarElementosDisabled(elementos) {
  elementos.forEach((elemento) => {
    elemento.disabled = true;
  })
}

function disabledBotones(botones) {
  botones.forEach((boton) => {
    boton.disabled = !boton.disabled;
  });
}

//Obtener id de dispositivo por la clase
function idDispositivo(clases, cadena) {
  // Obtengo la primera clase que incluye la cadena
  let claseBoton = clases.split(" ").find((clase) => {
    //retorno la condicion, si es true, find retornara la clase actual y cierra la busqueda, practicamente retorna el primer valor que retorne true en la condicion
    return clase.includes(cadena);
  });
  // Si se encontró una clase, obtén el id reemplazando lo que ponga en la "cadena"
  // Si no se encontró ninguna clase, asigna un valor predeterminado de 0
  return claseBoton ? claseBoton.replace(cadena, "") : 0;
}

//Evento de boton "Ver" (solo un boton)
function eventoVerDispoBtn(boton) {
  const botonesModalDispo = document.querySelectorAll(
    'button[class*="modalDispo"]'
  );
  const modalDispo = document.querySelector("#modalDispoForm");
  const modalBody = modalDispo.querySelector(".modal-body");
  const divAcordeones = modalBody.querySelector("#carateristicas");
  const modalTitulo = modalDispo.querySelector(".modal-title");
  //creo el spiner de bootstrap
  const spanLoading = F.spnCargando();

  boton.addEventListener("click", function (e) {
    e.preventDefault();
    boton.appendChild(spanLoading);
    boton.disabled = true;
    desactivarElementosDisabled(botonesModalDispo);
    let idDispo = idDispositivo(boton.className, "modalDispo");

    //con el id del dispositivo mando una petición con fetch para obtener la información del boton
    // Crea una nueva instancia del modal
    let modal = new bootstrap.Modal(modalDispo);
    //Aqui pongo los valores del dispositivo en el formulario
    //funcion de js/funciones.js
    P.peticionPost(
      window.location.pathname,
      { id: idDispo, action: "datosDispo" },
      (data) => {
        let dispo = data.dispositivo;
        modalTitulo.textContent = data.nombre;

        let acordeones = ``; //donde voy a crear el acordeon
        for (const key in dispo) {
          // recorro los datos pasados por la peticion, con el for in para extraer el key, o clave
          if (dispo.hasOwnProperty(key)) {
            const value = dispo[key]; // obtengo el valor de esa clave
            acordeones += acordeon(valoresTextos[key], value); //le paso la clave y el valor a la funcion para crear el acordeon y luego sumarlo a los acordeones
          }
        }
        divAcordeones.textContent = "";
        divAcordeones.insertAdjacentHTML("afterbegin", acordeones);
        modal.show();
      },
      () => {
        //activar boton y botones
        boton.disabled = false;
        activarElementosDisabled(botonesModalDispo);
        //quito el spinner del boton
        boton.removeChild(spanLoading);
      },
      //formdata
      false
    );
  });
}

//Evento de los botones de "Ver" de los dispositivos
function eventoVerDispo() {
  const botonesModalDispo = document.querySelectorAll(
    'button[class*="modalDispo"]'
  );

  botonesModalDispo.forEach((boton) => {
    //activar los botones
    boton.disabled = false;
    eventoVerDispoBtn(boton);
  });
}

//Evento de boton "Eliminar" (solo un boton)
function eventoEliminarDispoBtn(boton) {
  const btnSubmit = document.querySelector("#btn-form-juegos"),
    inputForm = document.querySelector("#formFile"),
    botonesEliminarDispo = document.querySelectorAll(
      'button[class*="eliminarDispo"]'
    ),
    contenedor = document.querySelector(".contenedorDispo");

  boton.addEventListener("click", (e) => {
    e.preventDefault();
    //deshabilitar el boton deL formulario e input
    btnSubmit.disabled = true;
    inputForm.disabled = true;

    //creo el spiner de bootstrap
    const spanLoading = F.spnCargando();
    boton.appendChild(spanLoading);
    boton.disabled = true;
    desactivarElementosDisabled(botonesEliminarDispo);
    let idDispo = idDispositivo(boton.className, "eliminarDispo");

    //funcion de js/funciones.js
    P.peticionPost(
      window.location.pathname,
      { id: idDispo, action: "eliminar" },
      (data) => {
        if (data.eliminacion) {
          const divDispo = contenedor.querySelector(`.dispoCont${idDispo}`);
          contenedor.removeChild(divDispo);
          let divDispoCount = contenedor.querySelectorAll(
            '[class*="dispoCont"]'
          ).length;
          if (divDispoCount == 0) {
            contenedor.textContent = "";
            contenedor.insertAdjacentHTML(
              "afterbegin",
              "<h2>Sin dispositivos</h2>"
            );
          }
        }
      },
      () => {
        activarElementosDisabled(botonesEliminarDispo);
        //activar formulario
        btnSubmit.disabled = false;
        inputForm.disabled = false;
      },
      //form data
      false
    );
  });
}

//Evento de los botones de "Eliminar" de los dispositivos
function eventoEliminarDispo() {
  const botonesEliminarDispo = document.querySelectorAll(
    'button[class*="eliminarDispo"]'
  );

  botonesEliminarDispo.forEach((boton) => {
    //activar los botones
    boton.disabled = false;
    eventoEliminarDispoBtn(boton);
  });
}

function dispoModal() {
  eventoVerDispo();
  eventoEliminarDispo();
}

function mostrarDispo(id, nombre, contenedor) {
  //creo el div de cada card de los dispositivos
  const cardDispo = document.createElement("div");
  cardDispo.classList.add("w-auto", "mx-2", "mb-3", `dispoCont${id}`);
  cardDispo.insertAdjacentHTML(
    "beforeend",
    `<div class="card">
      <div class="card-body">
        <h5 class="card-title">${nombre}</h5>
      </div>
      <div class="card-footer">
      </div>
    </div>`
  );
  //creo los botones para asignarle su respectivo evento
  //Boton ver
  const btnVer = document.createElement("button");
  btnVer.textContent = "Ver";
  btnVer.classList.add("btn", "btn-primary", `modalDispo${id}`);
  eventoVerDispoBtn(btnVer);

  //Boton eliminar
  const btnEliminar = document.createElement("button");
  btnEliminar.textContent = "Eliminar";
  btnEliminar.classList.add("btn", "btn-danger", `eliminarDispo${id}`);
  eventoEliminarDispoBtn(btnEliminar);

  //Agregar botones al card-footer del card del dispositivo
  const cardFooter = cardDispo.querySelector(".card-footer");
  cardFooter.insertAdjacentElement("afterbegin", btnVer);
  cardFooter.insertAdjacentElement("beforeend", btnEliminar);

  // crear el dispositivo con el createElement para agregarle el evento aqui y no varias veces con el dispoModal

  //preguntar cuantos dispositivos hay, si hay 0, limpio y agrego
  const dispositivos = contenedor.querySelectorAll('[class*="dispoCont"]');

  if (dispositivos.length == 0) {
    contenedor.textContent = "";
    contenedor.insertAdjacentElement("afterbegin", cardDispo);
  } else {
    contenedor.insertAdjacentElement("beforeend", cardDispo);
  }
}

document.addEventListener("DOMContentLoaded", function (e) {
  const btnSubmit = document.getElementById("btn-form-juegos");
  btnSubmit.disabled = false;
  const contenedorDispo = document.querySelector(".contenedorDispo");

  // Evento de ver y eliminar de cada card de los dispositivos
  dispoModal();

  //formulario de subida
  const form = document.querySelector("#envioTxt")
  //evento submit
  form.addEventListener("submit", (e) => {
    e.preventDefault();
    P.peticionFormPost(
      // le paso los valores requeridos
      "envioTxt", // id formulario
      urlProcesarDispo, //url hacia donde va a mandar la petición
      // la funcion a realizar
      (data) => {
        //creo la funcion la cual se la voy a pasar a la funcion de enviar peticion post
        //agregar el dispositivo
        mostrarDispo(data.id, data.nombre, contenedorDispo);
        // mensaje de guardado
        const Toast = Swal.mixin({
          toast: true,
          position: "bottom-end",
          showConfirmButton: false,
          timer: 3000,
          timerProgressBar: true,
          didOpen: (toast) => {
            toast.addEventListener("mouseenter", Swal.stopTimer);
            toast.addEventListener("mouseleave", Swal.resumeTimer);
          },
        });
        Toast.fire({
          icon: "success",
          title: `Dispositivo <i>${data.nombre}</i> guardado`,
        });
      },
      //resetForm
      true,
      //si sale "error" en la data
      (data) => {
        if (data.error[0] == "dipositivo ya existe") {
          Swal.fire({
            title: "El dispositivo ya existe, ¿Desea reemplazarlo?",
            showDenyButton: true,
            confirmButtonText: "Si",
            denyButtonText: `No`,
          }).then((result) => {
            if (result.isConfirmed) {
              //obtengo el formulario para enviar el archivo de nuevo
              const formArchivo = document.getElementById("envioTxt");
              const formdata = new FormData(formArchivo);
              formdata.append("reemplazar", "true");
              P.peticionPost(
                urlProcesarDispo,
                formdata,
                (data) => {
                  formArchivo.reset();
                  const Toast = Swal.mixin({
                    toast: true,
                    position: "bottom-end",
                    showConfirmButton: false,
                    timer: 3000,
                    timerProgressBar: true,
                    didOpen: (toast) => {
                      toast.addEventListener("mouseenter", Swal.stopTimer);
                      toast.addEventListener("mouseleave", Swal.resumeTimer);
                    },
                  });
                  Toast.fire({
                    icon: "success",
                    title: `Dispositivo <i>${data.nombre}</i> modificado`,
                  });
                },
                null,
                true
              );
            } else if (result.isDenied) {
              const formArchivo = document.getElementById("envioTxt");
              formArchivo.reset();
            }
          });
        } else {
          Swal.fire({
            icon: "error",
            title: "Oops...",
            text: data.error,
          });
        }
      }
    );
  })
  
});
