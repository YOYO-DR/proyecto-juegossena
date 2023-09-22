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
      <button data-slug="${juego.slug}" class="hover_scale btn-hidden me-3 text-danger"><i class="fs-5 bi-trash"></i></button>
  </div>
  `;
}

function eventoClickRadios(e) {
  const radios = document.querySelectorAll(`.form-check input[type="radio"`)
  const divCarrusel = document.querySelector(".div-derecha");
  const btnElimnar = document.querySelectorAll(".form-check button");
  
  //agregar evento para ver el carrusel
  radios.forEach((radio) => {
    radio.addEventListener("click", () => {
      //agregar plantilla de carga a las imagenes y radios

      //label del radio que se dio click
      const label = radio.nextElementSibling;

      //btn de eliminar juego
      const btnEliminar = label.nextElementSibling;

      //desactivar el boton de eliminar
      btnEliminar.disabled = true;
      btnEliminar.classList.replace("text-danger", "text-secondary");
      btnEliminar.classList.remove("hover_scale");
      
      //poner spinner al label
      const spn = spnCargando()
      label.appendChild(spn)
      
      //poner clase disabled al todos los form-check de los radios
      radios.forEach((radio) => {
        radio.closest(".form-check").classList.add("disabled")
        radio.disabled=true
      })
      
      //poner la plantilla de carga
      //limpiar div de carrusel
      divCarrusel.textContent = ''
      divCarrusel.insertAdjacentHTML("afterbegin", `
      <img
          class="img-fluid rounded img-carga"
          src="https://djangoyoiner.blob.core.windows.net/juegossena/static/media/img/empty-card.jpg"
          alt="Imagen de carga"
        />
        <h5 class="placeholder-glow w-75 text-center">
          <span class="placeholder col-10 "></span>
        </h5>`)

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
            `<h5 class="fs-3 text-center mt-3">
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
        () => {
          //quitar spn al label
          label.removeChild(spn);

          //quitar la clase disabed
          radios.forEach((radio) => {
            radio.closest(".form-check").classList.remove("disabled");
            radio.disabled = false;
          });

          //activar btn eliminar
          btnEliminar.disabled = false;
          btnEliminar.classList.replace("text-secondary", "text-danger");
          btnEliminar.classList.add("hover_scale");
        },
        (formdata = false)
      );
    })
  })

  //agregar evento de eliminar favorito
  btnElimnar.forEach((btn) => {
    btn.addEventListener("click", () => { 
      const slug_juego = btn.getAttribute("data-slug");
      const radio = document.querySelector(`[data-slug="${slug_juego}"]`);
      const nombre_juego = btn.previousElementSibling.textContent.trim()
      //Alerta de sweetalert para confirmar la eliminación

      Swal.fire({
        title: `Eliminar`,
        html: `¿Desea eliminar <i>${nombre_juego}</i> de los favoritos?`,
        showCancelButton: true,
        confirmButtonText: "Confirmar"
      }).then((result) => {
        /* Read more about isConfirmed, isDenied below */
        if (result.isConfirmed) {
          //desactivar el boton
          //manda la peticion
          // desactivar input, disabled al form-check, desactivar boton eliminar, hover_scale quitar al btn_eliminar, eliminar el form-check, traer el padre y el form-chect con el closets aqui para solo llamrlos si se confirma la eliminacion
        }
      });

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