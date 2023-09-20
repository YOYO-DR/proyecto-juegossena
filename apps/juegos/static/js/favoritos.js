// funcion para cuando se cambie de carrusel : activarCarrusel(".btn-left",".btn-right","#slider",".slider-section",".carruseles");

function plantillaCarrusel(imagenes) {
  let sliders = ``;
  for (let imagen of imagenes) {
    sliders += `<section class="slider-section">
          <img src="${imagen}" alt="">
        </section>`;
  }
  let plantilla = `<div class="container-carousel col-12 col-md-6">
      
      <div class="carruseles" id="slider">
        ${sliders}
      </div>
      <div class="btn-left"><i class="bi bi-caret-left-fill"></i></div>
      <div class="btn-right"><i class="bi bi-caret-right-fill"></i></div>
    </div>
</div>`;
  return plantilla
}