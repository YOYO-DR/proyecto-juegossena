//constantes
const btnLeft = document.querySelector(".btn-left"),
  btnRight = document.querySelector(".btn-right"),
  slider = document.querySelector("#slider"),
  sliderSections = document.querySelectorAll(".slider-section"),
  carruseles = document.querySelector(".carruseles");

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
