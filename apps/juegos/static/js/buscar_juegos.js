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

//height de cada checkbox
function heightCheckbox(checkbox) {
  let sumaHeight = 0
  checkbox.forEach((check) => { 
    sumaHeight += check.offsetHeight;
  })
  return sumaHeight;
}

document.addEventListener("DOMContentLoaded", (e) => {
  //constantes
  const radioInputs = document.querySelectorAll('input[name="dispo');
  const opciones = document.querySelector(".opciones");
  const botonOpciones = opciones.querySelector("button");
  let sumaCheckbox = heightCheckbox(opciones.querySelectorAll(".form-check"));
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

  let botonOpcionesHeight = botonOpciones.offsetHeight; // obtén la altura del botón
  opciones.style.maxHeight = `${botonOpcionesHeight}px`;
  //boton de las opciones
  botonOpciones.addEventListener("click", (e) => {
    if (opciones.classList.contains("activa")) {
      opciones.style.maxHeight = `${botonOpcionesHeight}px`; // establece la altura máxima al tamaño del botón
    } else {
      opciones.style.maxHeight = (sumaCheckbox+(sumaCheckbox*0.4))+"px"; // establece la altura máxima a un valor muy grande
    }
    opciones.classList.toggle("activa");
  });
})