// funcion para cuando se cambie de carrusel : activarCarrusel(".btn-left",".btn-right","#slider",".slider-section",".carruseles");

function plantillaCarrusel(imagenes) {
  let sliders = ``;
  for (const imagen of imagenes) {
    sliders += `
      <section class="slider-section">
        <img src="${imagen}" alt="">
      </section>`;
  }
  let plantilla = `
  <div class="container-carousel col-12 col-md-6">
    <div class="carruseles" id="slider">
      ${sliders}
    </div>
    <div class="btn-left"><i class="bi bi-caret-left-fill"></i></div>
    <div class="btn-right"><i class="bi bi-caret-right-fill"></i></div>
  </div>`;
  return plantilla;
}

function plantillaRadioJuego(juego) {
  return `
  <div class="form-check">
    <input
      class="form-check-input"
      type="radio"
      name="dispo"
      id="${juego.id}"
    />
      <label class="form-check-label w-100" for="${juego.id}">
        ${juego.nombre}
      </label>
  </div>
  `;
}

document.addEventListener("DOMContentLoaded", function () {
  //constantes
  const divRadios = document.querySelector(".div-izquierda div");
  const divRadiosH2 = document.querySelector(".div-izquierda h2")
  const divCarrusel = document.querySelector(".div-derecha")

  //hacer peticion para traer los juegos de favoritos
  peticionPost(
    //url
    ".",
    //datos a enviar
    {action:"juegos"},
    (data) => { 
      divRadiosH2.innerHTML =
        data.juegos.length > 0
          ? `Juegos agregados (${data.juegos.length})`
          : `Sin juegos agregados`;

      divRadios.innerHTML=``
      for (let i = 0; i < data.juegos.length;i++) {
        divRadios.innerHTML += plantillaRadioJuego(data.juegos[i]);
      }
      
    },
    (funcionFinal = null),
    (formdata = false));
})