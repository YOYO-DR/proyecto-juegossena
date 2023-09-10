//constantes DOM
  const listaRequi = document.querySelector(".lista-requi"),
  btnAgregarFav = document.querySelector("#agre-favo");

//lista de requisitos
let lis_requi = "";
peticionPost(
  ".",
  {
    action: "requisitos"
  },
  (data) => {
    //el Object.entries coje el objeto y crea un arreglo de pares [[clave,valor],[clave,valor]] y asi hago destructuración por cada recorrido y obtengo la clave y el valor del objeto
    for (const [clave, valor] of Object.entries(data.juego)) {
      // recordar que valoresTextos esta en funciones.js y es una constante con los valores que se recibe del servidor y que los paso a palabras para mostrar
      lis_requi += `<li><strong>${valoresTextos[clave]}:</strong> ${valor}</li>`;
    }
    listaRequi.innerHTML = lis_requi;
  },
  (funcionFinal = null),
  (formdata = false)
);

//evento para guardar el favorito de un juego
btnAgregarFav.addEventListener("click", function (e) {
  e.preventDefault();
  const spn=spnCargando()
  btnAgregarFav.appendChild(spn);
  btnAgregarFav.disabled = true;
  //aqui se envia la petición - action: agrefav
  peticionPost(
    ".",
    { action: "agrefav" },
    (data) => {
      btnAgregarFav.removeChild(spn);
      const i_corazon = btnAgregarFav.querySelector("i");
      //para cambiar el icono del corazon
      if (data.fav == "agregado") {
        i_corazon.classList.remove("bi-heart");
        i_corazon.classList.add("bi-heart-fill", "text-danger");
      } else if (data.fav == "quitado") {
        i_corazon.classList.remove("bi-heart-fill", "text-danger");
        i_corazon.classList.add("bi-heart");
      }
    },
    () => {
      btnAgregarFav.disabled = false
      //pregunto si existe el spinner en el botón y quitarlo
      const spinner = btnAgregarFav.querySelector("spinner-border");
      if (spinner) {
        btnAgregarFav.removeChild(spinner)
      }
    },
    (formdata = false)
  );
});