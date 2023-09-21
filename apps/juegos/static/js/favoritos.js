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
      data-slug="${juego.slug}"
      name="dispo"
      id="${juego.id}"
    />
      <label class="form-check-label w-100" for="${juego.id}">
        ${juego.nombre}
      </label>
      <button class="btn-hidden me-3 text-danger"><i class="fs-5 bi-trash"></i></button>
  </div>
  `;
}

function eventoClickRadios(e) {
  const radios = document.querySelectorAll(`.form-check input[type="radio"`)
  const divCarrusel = document.querySelector(".div-derecha");
  //agregar evento
  radios.forEach((radio) => {
    radio.addEventListener("click", () => {
      //agregar plantilla de carga a las imagenes y radios

      //Ejecutar lo del carrusel
      //hacer peticion para pedir las imagenes del juego
      peticionPost(
        //url
        ".",
        //datos a enviar
        {
          action: "imagenes",
          slug: radio.getAttribute("data-slug"),
        },
        (data) => {
          //Limpio el div del carrusel
          divCarrusel.textContent = "";
          //le agrego el carrusel
          divCarrusel.insertAdjacentHTML(
            "beforeend",
            plantillaCarrusel(data.imagenes)
          );
          //agregar h2 con el nombre y direccion del juego
          divCarrusel.insertAdjacentHTML(
            "beforeend",
            `<h5 class="fs-3 text-center">
              <a href="/juegos/detalle/${data.juego.slug}" class="link">${data.juego.nombre}</a>
             </h5>
            `
          );
          //activar carrusel
          activarCarrusel(
            ".btn-left",
            ".btn-right",
            "#slider",
            ".slider-section",
            ".carruseles"
          );
        },
        (funcionFinal = null),
        (formdata = false)
      );
    })
  })
}

document.addEventListener("DOMContentLoaded", function () {
  //constantes
  const divRadios = document.querySelector(".div-izquierda div");
  const divRadiosH2 = document.querySelector(".div-izquierda h2")

  //hacer peticion para traer los juegos de favoritos
  peticionPost(
    //url
    ".",
    //datos a enviar
    { action: "juegos" },
    // funcion para poner los radios de los juegos en favoritos
    (data) => {
      // limpio el elemento pero sin utilizar innertHtml, no es optimo utilizar innerHTML porque este llama al analizador HTML y en rendimiento disminuye, mejor textContent ya que no analiza nada porque solo el texto
      divRadiosH2.textContent = "";
      divRadiosH2.insertAdjacentHTML(
        "afterbegin",
        data.juegos.length > 0
          ? `Juegos agregados (${data.juegos.length})`
          : `Sin juegos agregados`
      );

      divRadios.textContent = "";
      for (let i = 0; i < data.juegos.length; i++) {
        divRadios.insertAdjacentHTML(
          "beforeend",
          plantillaRadioJuego(data.juegos[i])
        );
      }
      //despues de la peticion agregar el evento a los radios
      eventoClickRadios();
    },
    (funcionFinal = null),
    (formdata = false));
})