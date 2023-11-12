//Inicializo la clase de peticiones
const P = new Peticiones();

class modalBootstrap5 {
  constructor(modal, title, body) {
    this.title = title;
    this.body = body;
    this.modal = document.getElementById(modal); // <div id="modal"></div>
    this.plantillaElement(); //generar el modal
  }

  show() {
    let bootstrap_modal = new bootstrap.Modal(this.modal);
    bootstrap_modal.show();
  }

  plantillaElement() {
    // agregar atributos al div del modal
    this.modal.classList.add("modal", "fade");
    this.modal.setAttribute("tabindex", "-1");
    this.modal.setAttribute("aria-labelledby", "ModalLabel");
    this.modal.setAttribute("aria-hidden", "true");

    // modal dialog
    let modal_dialog = document.createElement("div");
    modal_dialog.classList.add("modal-dialog");
    //insertar en el modal
    this.modal.textContent = "";
    this.modal.appendChild(modal_dialog);

    //modal content
    let modal_content = document.createElement("div");
    modal_content.classList.add("modal-content", "bg-black");
    //insertarlo dentro del modal dialog
    modal_dialog.appendChild(modal_content);

    //modal header
    let modal_header = document.createElement("div");
    modal_header.classList.add("modal-header");
    //insertarlo dentro del modal content
    modal_content.appendChild(modal_header);

    //h1 - modal title
    let h1 = document.createElement("h1");
    h1.classList.add("modal-title", "fs-5");
    h1.setAttribute("id", "ModalLabel");
    h1.insertAdjacentHTML("afterbegin", this.title);
    //insertar en el modal header
    modal_header.insertAdjacentElement("afterbegin", h1);

    //btn close - modal header
    let btn_close = document.createElement("button");
    btn_close.classList.add("btn-close", "bg-white");
    btn_close.setAttribute("data-bs-dismiss", "modal");
    btn_close.setAttribute("aria-label", "Close");
    //insertar en el modal header
    modal_header.insertAdjacentElement("beforeend", btn_close);

    //modal body
    let modal_body = document.createElement("div");
    modal_body.classList.add("modal-body");
    modal_body.insertAdjacentHTML("afterbegin", this.body);
    // si la nota viene con imagenes, les pongo la clase img-fluid
    let imagenes_body = modal_body.querySelectorAll("img");
    if (imagenes_body.length > 0) {
      imagenes_body.forEach((img) => {
        if (!img.classList.contains("img-fluid"))
          img.classList.add("img-fluid");
      })
    }
    //insertar en el final del modal content
    modal_content.insertAdjacentElement("beforeend", modal_body);
  }
}

/* crear objeto para crear un modal con createelement y ponerlo antes del cierre del body para luego mostralo*/
//funciones

function quitarTildes(str) {
    //objeto con las vocales y su expresión regular para quitar las tildes
    let mapaAcentosHex = {
      a: /[\xE0-\xE6]/g,
      e: /[\xE8-\xEB]/g,
      i: /[\xEC-\xEF]/g,
      o: /[\xF2-\xF6]/g,
      u: /[\xF9-\xFC]/g,
      A: /[\xC0-\xC6]/g,
      E: /[\xC8-\xCB]/g,
      I: /[\xCC-\xCF]/g,
      O: /[\xD2-\xD6]/g,
      U: /[\xD9-\xDC]/g,
    };
  for (let letra in mapaAcentosHex) {
      // obtengo cada expresión regular y se la aplico a la cadena deseada y asi quitar todas las tildes
      let expresionRegular = mapaAcentosHex[letra];
      str = str.replace(expresionRegular, letra);
    }
    return str;
  
}

document.addEventListener("DOMContentLoaded", (e) => {
  const preguntas = document.querySelectorAll(".preguntas a");
  const input = document.querySelector(".input-group input");
  // evento para ver cada respuesta
  preguntas.forEach((pregunta) => {
    pregunta.addEventListener("click", (e) => {
      e.preventDefault();
      //spn cargando
      let spn = F.spnCargando();
      //ponerlo al final de la pregunta
      pregunta.insertAdjacentElement("beforeend", spn);
      //inhabilitar todos los links
      preguntas.forEach((pregunta) => {
        pregunta.classList.add("link-disabled");
      });
      // id de la pregunta
      let id = pregunta.getAttribute("data-id");
      //funcion despues de la peticion
      const funcion = (data) => {
        let modal = new modalBootstrap5("modal", data.pregunta, data.respuesta);
        modal.show();
      };
      //mandar peticion
      P.peticionPost(
        window.location.pathname,
        { id: id },
        funcion,
        () => {
          //habilitar todos los links
          preguntas.forEach((pregunta) => {
            pregunta.classList.remove("link-disabled");
          });
          pregunta.removeChild(spn);
        },
        (formdata = false)
      );
    });
  });

  //evento para buscar mientras escribe
  input.addEventListener("input", (e) => {
    let bus = quitarTildes(input.value)
      .toLowerCase()
      .trim();
    if (bus !== "") {
      preguntas.forEach((pregunta) => {
        //quitar las tildes
        const normalizar = quitarTildes(pregunta.textContent)
          .toLowerCase();
        console.log(normalizar)
        if (normalizar.includes(bus)) {
          console.log(normalizar);
          if (pregunta.classList.contains("hidden")) {
            pregunta.classList.remove("hidden");
          }
        } else {
          if (!pregunta.classList.contains("hidden")) {
            pregunta.classList.add("hidden");
          }
        }
      });
    } else {
      preguntas.forEach((pregunta) => {
        if (pregunta.classList.contains("hidden"))
          pregunta.classList.remove("hidden");
      });
    }
  });
});
