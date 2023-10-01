class Funciones {
  constructor() {
    this.csrftoken=this.obtenerCsrfToken()
  }
  //notificacion o modal de notificacion para los mensajes
  mensajeSweet(mensaje, icono) {
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
      icon: icono,
      title: mensaje,
    });
  }

  //para que pueda obtener el token, debe estar el {% csrf_token %} en el formulario para que este en las cookies tambien
  obtenerCsrfToken() {
    let csrfCookie = document.cookie
      .split(";")
      .find((cookie) => cookie.trim().startsWith("csrftoken="));
    // si no esta en la cookie, la obtengo del input oculto, y si tampoco, retorno null
    if (!csrfCookie) {
      csrfCookie = document.querySelector("[name=csrfmiddlewaretoken]");
      if (!csrfCookie) {
        console.error("CSRF token not found in cookies.");
        return null;
      }
      return csrfCookie.value;
    }
    return csrfCookie.split("=")[1];
  }

  //enviar peticion post pero fuera de un formulario
  peticionPost(
    url,
    datos,
    funcion,
    funcionFinal = null,
    formdata = false
  ) {
    datos = formdata == true ? datos : JSON.stringify(datos);
    fetch(url, {
      method: "POST",
      headers: {
        "X-CSRFToken": this.csrftoken,
      },
      body: datos,
    })
      //si la respuesta es correcta, convierto a json/objeto
      .then((response) => response.json())
      //si se convierte correctamente, ejecuto la función y le paso la data
      .then((data) => {
        if ("error" in data) {
          if (data.error == "no-auth") {
            window.location.href = `/usuarios/iniciarsesion/?next=${window.location.pathname}`;
          }
          this.mensajeSweet(data.error, "error");
        } else {
          funcion(data);
        }
      })
      //si sale un error lo paso por consola
      .catch((error) => {
        this.mensajeSweet(error, "error");
      })
      .finally(() => {
        if (funcionFinal != null) {
          funcionFinal();
        }
      });
  }

  //enviar post desde un formulario, lo ejecuto apenas cargue el forulario porque el agrega el evento del submit
  peticionFormPost(idForm, url, funcion, resetForm = true) {
    const form = document.getElementById(idForm);
    const inputs = form.querySelectorAll("input");

    form.addEventListener("submit", async (e) => {
      e.preventDefault();
      //obtengo el boton del formulario
      const btnSubmit = form.querySelector('button[type="submit"]');
      //creo el spiner de bootstrap
      const spanLoading = this.spnCargando();
      //Agrego el valor del boton mas el spinner
      btnSubmit.appendChild(spanLoading);
      //deshabilito el boton
      btnSubmit.disabled = true;
      const formData = new FormData(form);
      //inhabilito los inputs despues de obtener sus valores
      inputs.forEach((input) => {
        input.disabled = true;
      });
      fetch(url, {
        method: "POST",
        headers: {
          "X-CSRFToken": this.csrftoken,
        },
        body: formData,
      })
        .then((response) => response.json())
        .then((data) => {
          if (!("error" in data)) {
            if (resetForm == true) {
              form.reset();
            }
            funcion(data); //ejecutar funcion si la respuesta es correcta
          } else {
            this.mensajeSweet(data.error, "error");
          }
        })
        .catch((error) => {
          this.mensajeSweet(error, "error");
        })
        .finally(() => {
          //habilito los inputs
          inputs.forEach((input) => {
            input.disabled = false;
          });
          //habilito el boton
          btnSubmit.disabled = false;
          //dejo ahora solo el valor del botón
          btnSubmit.removeChild(spanLoading);
        });
    });
  }

  // poner en mayuscula la primera letra de un string
  toTitle(str) {
    return str.charAt(0).toUpperCase() + str.slice(1);
  }

  //para crear un spn como Nodo y asi quitarlo y ponerlo facil sin necesidad del "innerHTML"
  //por si quiere poner clases al spinner
  spnCargando(clases = null) {
    const spn = document.createElement("div");
    spn.classList.add("ms-1", "spinner-border", "spinner-border-sm");
    if (clases) {
      clases.forEach((clase) => {
        spn.classList.add(clase);
      });
    }
    spn.setAttribute("role", "status");
    spn.insertAdjacentHTML(
      "afterbegin",
      '<span class="visually-hidden">Loading...</span>'
    );
    return spn;
  }
}

//objeto con los valores que se obtienen del servidor pero ya para mostrar
const valoresTextos = {
  tipo: "Tipo",
  tamano: "Tamaño",
  velocidad: "Velocidad",
  capacidad: "Capacidad",
  nombre: "Nombre",
  cantidadNucleos: "Cantidad de núcleos",
  velocidadNucleo: "Velocidad de núcleo",
  velocidadMemoria: "Velocidad de memoria",
  hilos: "Hilos",
  modelo: "Modelo",
  nucleos: "Núcleos",
  velocidadMaxima: "Velocidad de máxima",
  so: "Sistema operativo",
  ram: "Ram",
  procesador: "Procesador",
  grafica: "Tarjeta gráfica",
  espaciore: "Espacio requerido",
  espacio: "Espacio",
};

//Inicializo la clase
const F = new Funciones();

//Funciones del menu
document.addEventListener("DOMContentLoaded", function () {
  const botonMenu = document.getElementById("btnmenu");
  const containerMenu = document.getElementById("container-menu");

  botonMenu.addEventListener("click", function (e) {
    e.preventDefault();
    containerMenu.classList.toggle("es_activo");
  });
});
