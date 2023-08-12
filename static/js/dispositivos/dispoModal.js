//acordeon
function acordeon (nombre, valores) {
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
        ul += `<li><b>${key}</b>: ${value}</li>`; // agrego los valores
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
          data-bs-target="#collapse${nombre}"
          aria-expanded="false"
          aria-controls="collapseOne"
          >
           ${nombre}
          </button>
          </h2>
          <div
          id="collapse${nombre}"
          class="accordion-collapse collapse"
          data-bs-parent="#carateristicas"
          >
          <div class="accordion-body">
          ${ul}
          </div>
          </div>
          </div>`;
  return acor; // retorno el acordeon creado
};

//activar - desactivar botones
function disabledBotones(botones) {
  botones.forEach((boton) => {
    boton.disabled = !boton.disabled
  })
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

      //obtengo el valor inicial del boton
      let valorBoton = boton.innerHTML;
      //creo el spiner de bootstrap
      let spanLoading = `<div class="ms-1 spinner-border spinner-border-sm" role="status">
          <span class="visually-hidden">Loading...</span>
        </div>`;
      boton.innerHTML = `${valorBoton}${spanLoading}`;
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
          if (data.dispositivo) {
            let dispo = data.dispositivo;
            modalTitulo.innerHTML = data.nombre;

            let acordeones = ``; //donde voy a crear el acordeon
            for (const key in dispo) {
              // recorro los datos pasados por la peticion, con el for in para extraer el key, o clave
              if (dispo.hasOwnProperty(key)) {
                const value = dispo[key]; // obtengo el valor de esa clave
                acordeones += acordeon(key, value); //le paso la clave y el valor a la funcion para crear el acordeon y luego sumarlo a los acordeones
              }
            }
            divAcordeones.innerHTML = acordeones;
            modal.show();
          } else {
            alert(data.error);
          }
        },
        //formdata
        false,
        () => {
          //quito el spinner del boton
          disabledBotones(botonesModalDispo);
          boton.innerHTML = valorBoton;
        }
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

      //obtengo el valor inicial del boton
      let valorBoton = boton.innerHTML;
      //creo el spiner de bootstrap
      let spanLoading = `<div class="ms-1 spinner-border spinner-border-sm" role="status">
          <span class="visually-hidden">Loading...</span>
        </div>`;
      boton.innerHTML = `${valorBoton}${spanLoading}`;
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
              let h2 = document.createElement("h2");
              h2.innerHTML = "Sin dispositivos";
              contenedor.appendChild(h2);
              const tituloH1 = document.getElementById("tituloH1");
              tituloH1.innerHTML = "Dispositivos";
            }
          }
        },
        false,
        () => {
          disabledBotones(botonesEliminarDispo);
          boton.innerHTML = valorBoton;
          //activar formulario
          btnSubmit.disabled = false;
          inputForm.disabled = false;
        }
      );
    });
  });
}

function mostrarDispo(id, nombre, contenedor) {
  let plantilla = `
  <div class="col col-sm-6 col-md-4 mb-3 dispoCont${id}">
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
  contenedor.innerHTML+=plantilla
}