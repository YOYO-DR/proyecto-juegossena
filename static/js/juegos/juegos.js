//obtener el script
const scriptElement = document.currentScript;

//obtengo los valores de data
const urlBuscarJuegos = scriptElement.getAttribute("data-urlbuscarjuegos");

//constantes DOM
const btnLeft = document.querySelector(".btn-left"),
  btnRight = document.querySelector(".btn-right"),
  slider = document.querySelector("#slider"),
  sliderSections = document.querySelectorAll(".slider-section"),
  carruseles = document.querySelector(".carruseles"),
  listaRequi = document.querySelector(".lista-requi"),
  btnAgregarFav = document.querySelector("#agre-favo");

//carrusel
//calcular imagenes y cambiar el css
sliderSections.forEach(function (section) {
  section.style.width = `calc(100%/${sliderSections.length})`;
});
carruseles.style.width = `${100 * sliderSections.length}%`;

let operacion = 0,
  counter = 0,
  widthImg = 100 / sliderSections.length;

function moveToRight() {
  if (counter >= sliderSections.length - 1) {
    counter = 0;
    operacion = 0;
    slider.style.transform = `translate(${operacion}%)`;
    slider.style.transition = "none";
    //cerrar la ejecucion de la funcion aqui
    return;
  }
  counter++;
  operacion += widthImg;
  // poner estilos
  slider.style.transform = `translate(-${operacion}%)`;
  // para que el contenedor se mueva suavemente
  slider.style.transition = "all ease .6s";
}

function moveToLeft() {
  counter--;
  if (counter < 0) {
    counter = sliderSections.length - 1;
    operacion = widthImg * (sliderSections.length - 1);
    slider.style.transform = `translate(-${operacion}%)`;
    slider.style.transition = "none";
    //cerrar la ejecucion de la funcion aqui
    return;
  }
  operacion -= widthImg;
  slider.style.transform = `translate(-${operacion}%)`;
  slider.style.transition = "all ease .6s";
}
//que se ejecute cada 4 segundos
setInterval(function () {
  moveToRight();
}, 5000);

btnLeft.addEventListener("click", (e) => moveToLeft());
btnRight.addEventListener("click", (e) => moveToRight());

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
  let html_btn = btnAgregarFav.innerHTML;
  btnAgregarFav.innerHTML += `<div class="ms-1 spinner-border spinner-border-sm" role="status">
        <span class="visually-hidden">Loading...</span>
</div>`;
  btnAgregarFav.disabled = true;
  //aqui se envia la petición - action: agrefav
  peticionPost(
    ".",
    { action: "agrefav" },
    (data) => {
      btnAgregarFav.innerHTML = html_btn;
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