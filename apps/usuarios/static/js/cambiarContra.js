//obtener script y obtener la url del detalle juego
const urlIniciarSesion = document.currentScript.getAttribute(
  "data-url-iniciar-sesion"
);

//Inicializo la clase de peticiones
const P = new Peticiones();
document.addEventListener("DOMContentLoaded", function () {
  const form = document.querySelector("#form");
  const mensaje = document.querySelector("#mensaje");

  form.addEventListener("submit", (e) => {
    e.preventDefault();
    P.peticionFormPost(
      "form", // id formulario
      ".",
      (data) => {
        mensaje.className = "mensaje-correcto";
        let iniciarSesion = `<a href="${urlIniciarSesion}" class="link-primary">iniciar sesión</a>`;
        mensaje.insertAdjacentHTML(
          "afterbegin",
          `La contraseña se cambio correctamente, ya puedes ${iniciarSesion}`
        );
        form.remove();
      }
    );
  });
});
