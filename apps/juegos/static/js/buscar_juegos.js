//constantes
const radioInputs = document.querySelectorAll('input[name="dispo');

//evento de cuando se seleccione un radio
radioInputs.forEach((radio) => {
  radio.addEventListener("change", (e) => {
    //verifico si el radio esta seleccionado
    if (radio.checked) {
      const label = document.querySelector(
        `label[for="${radio.getAttribute("id")}"]`
      );
      radio.disabled=true
      const spn = spnCargando()
      label.appendChild(spn)
      setTimeout(() => {
        label.removeChild(spn)
        radio.disabled = false
      },2000)
    }
  });
});
