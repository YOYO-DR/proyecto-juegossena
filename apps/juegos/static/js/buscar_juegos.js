//constantes
const radioInputs = document.querySelectorAll('input[name="dispo');

//funciones
function desRadios() {
  radioInputs.forEach((radio) => {
    if (!radio.checked) {
      radio.disabled = true;
      radio.parentNode.classList.add("disabled")
    }
  });
}

function actRadios() {
  radioInputs.forEach((radio) => {
    if (!radio.checked) {
      radio.disabled = false;
      radio.parentNode.classList.remove("disabled");
    }
  });
}

//evento de cuando se seleccione un radio
radioInputs.forEach((radio) => {
  radio.addEventListener("change", (e) => {
    //desactivo los demás radios
    desRadios();
    //verifico si el radio esta seleccionado
    if (radio.checked) {
      const label = document.querySelector(
        `label[for="${radio.getAttribute("id")}"]`
      );
      radio.disabled=true
      const spn = spnCargando()
      label.appendChild(spn)
      //simulando peticion
      setTimeout(() => {
        label.removeChild(spn)
        radio.disabled = false
        //activar radios
        actRadios();
      },2000)
    }
  });
});
