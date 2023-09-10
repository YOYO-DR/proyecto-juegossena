//funciones
function actDesRadios(radioInputs,activar = true) {
  radioInputs.forEach((radio) => {
    if (!radio.checked) {
      radio.disabled = activar == true ? false : true;
      if (activar == true) {
        radio.parentNode.classList.remove("disabled");
      } else {
        radio.parentNode.classList.add("disabled");
      }
    }
  });
}

document.addEventListener("DOMContentLoaded", (e) => {
  //constantes
  const radioInputs = document.querySelectorAll('input[name="dispo');
  const opciones = document.querySelector(".opciones");
  const botonOpciones = opciones.querySelector("button");

  //evento de cuando se seleccione un radio
  radioInputs.forEach((radio) => {
    radio.addEventListener("change", (e) => {
      //desactivo los demás radios
      actDesRadios(radioInputs, (activar = false));
      //verifico si el radio esta seleccionado
      if (radio.checked) {
        const label = document.querySelector(
          `label[for="${radio.getAttribute("id")}"]`
        );
        radio.disabled = true;
        const spn = spnCargando();
        label.appendChild(spn);
        //simulando peticion
        setTimeout(() => {
          label.removeChild(spn);
          radio.disabled = false;
          //activar radios
          actDesRadios(radioInputs, (activar = true));
        }, 2000);
      }
    });
  });

  //boton de las opciones
  botonOpciones.addEventListener("click", (e) => {
    opciones.classList.toggle("activa");
  });
})