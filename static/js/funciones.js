//para que pueda obtener el token, debe estar el {% csrf_token %} en el formulario para que este en las cookies tambien
function obtenerCsrfToken() {
  const csrfCookie = document.cookie
    .split(";")
    .find((cookie) => cookie.trim().startsWith("csrftoken="));
  if (!csrfCookie) {
    console.error("CSRF token not found in cookies.");
    return null;
  }
  return csrfCookie.split("=")[1];
}

//enviar peticion post pero fuera de un formulario
function peticionPost(
  url,
  datos,
  funcion,
  formdata = false,
  funcionFinal = null
) {
  csrftoken = obtenerCsrfToken();
  datos = (formdata == true) ? datos : JSON.stringify(datos);
  fetch(url, {
    method: "POST",
    headers: {
      "X-CSRFToken": csrftoken,
    },

    body: datos,
  })
    //si la respuesta es correcta, convierto a json/objeto
    .then((response) => response.json())
    //si se convierte correctamente, ejecuto la función y le paso la data
    .then((data) => funcion(data))
    //si sale un error lo paso por consola
    .catch((error) => {
      console.error("Error: " + error);
    })
    .finally(() => {
      if (funcionFinal != null) {
        funcionFinal();
      }
    });
}

//enviar post desde un formulario, lo ejecuto apenas cargue el forulario porque el agrega el evento del submit
function peticionFormPost(idForm, url, funcion, resetForm = true) {
  let csrftoken = obtenerCsrfToken();
  const form = document.getElementById(idForm);
  const inputs = form.querySelectorAll("input");

  form.addEventListener("submit", async (e) => {
    e.preventDefault();
    //obtengo el boton del formulario
    const btnSubmit = form.querySelector('button[type="submit"]');
    //obtengo el valor inicial del boton
    let valorSubmit = btnSubmit.innerHTML;
    //creo el spiner de bootstrap
    let spanLoading = `<div class="ms-1 spinner-border spinner-border-sm" role="status">
  <span class="visually-hidden">Loading...</span>
</div>`;
    //Agrego el valor del boton mas el spinner
    btnSubmit.innerHTML = `${valorSubmit}${spanLoading}`;
    //deshabilito el boton
    btnSubmit.disabled = true;
    const formData = new FormData(form);
    //inhabilito los inputs despues de obtener sus valores
    inputs.forEach((input) => {
      input.disabled = true;
    });

    try {
      const response = await fetch(url, {
        method: "POST",
        headers: {
          "X-CSRFToken": csrftoken,
        },
        body: formData,
      });
      const data = await response.json();
      if (response.ok) {
        if (!("error" in data)) {
          if (resetForm == true) {
            form.reset();
          }
        }
        //habilito los inputs
        inputs.forEach((input) => {
          input.disabled = false;
        });
        funcion(data); //ejecutar funcion si la respuesta es correcta
      }
    } catch (error) {
      console.error("Error:", error);
    }
    //habilito el boton
    btnSubmit.disabled = false;
    //dejo ahora solo el valor del botón
    btnSubmit.innerHTML = `${valorSubmit}`;
  });
}

// poner en mayuscula la primera letra de un string
function toTitle(str) {
  return str.charAt(0).toUpperCase() + str.slice(1);
}