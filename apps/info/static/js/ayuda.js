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
    modal_content.classList.add("modal-content");
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
    btn_close.classList.add("btn-close");
    btn_close.setAttribute("data-bs-dismiss", "modal");
    btn_close.setAttribute("aria-label", "Close");
    //insertar en el modal header
    modal_header.insertAdjacentElement("beforeend", btn_close);

    //modal body
    let modal_body = document.createElement("div");
    modal_body.classList.add("modal-body");
    modal_body.insertAdjacentHTML("afterbegin", this.body);
    //insertar en el final del modal content
    modal_content.insertAdjacentElement("beforeend", modal_body);
  }
}

/* crear objeto para crear un modal con createelement y ponerlo antes del cierre del body para luego mostralo*/
//funciones

document.addEventListener("DOMContentLoaded", (e) => {
  const preguntas = document.querySelectorAll(".preguntas a");
  preguntas.forEach((pregunta) => {
    pregunta.addEventListener("click", (e) => {
      e.preventDefault();
      //spn cargando
      let spn = F.spnCargando()
      //ponerlo al final de la pregunta
      pregunta.insertAdjacentElement("beforeend", spn);
      //inhabilitar todos los links
      preguntas.forEach((pregunta) => {
        pregunta.classList.add("link-disabled");
      })
      // id de la pregunta
      let id = pregunta.getAttribute("data-id");
      //funcion despues de la peticion
      const funcion = (data) => {
        let modal = new modalBootstrap5(
          "modal",
          data.pregunta,
          data.respuesta
        );
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
});
