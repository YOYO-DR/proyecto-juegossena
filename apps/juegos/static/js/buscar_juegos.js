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

//realizar busqueda
function buscar(check, input) {
  //(check,radios,input)
  //check=id del checkbox del evento
  //radios = [lista y pregunto cual es el precionado ya que solo seria 1]
  //input = div.input-group de la busqueda > input y button{i del icono}

  const ckeckboxs = document.querySelectorAll(`input[type="checkbox"]`);

  //ejecuto la busqueda solo si el input tiene datos
  if (input.value.trim()) {
    //buscar
    //desactivar
    //spn del check
    let spnCheck = spnCargando();
    ckeckboxs.forEach((checkbox) => {
      if (checkbox.getAttribute("id") == check) {
        //le agrego el spinner
        checkbox.parentNode.querySelector("label").appendChild(spnCheck);
      }
      checkbox.disabled = true;
    });

    //desactivar input
    input.disabled = true;

    //hacer peticion
    setTimeout(() => {
      //activar checkboxs
      ckeckboxs.forEach((checkbox) => {
        if (checkbox.getAttribute("id") == check) {
          checkbox.parentNode.querySelector("label").removeChild(spnCheck);
        }
        checkbox.disabled = false;
        input.disabled = false;
      });
    }, 2000);
  } else {
    mensajeSweet("Debe ingresar un valor en la busqueda","warning");
  }
}

document.addEventListener("DOMContentLoaded", (e) => {
  //constantes
  const radioInputs = document.querySelectorAll('input[name="dispo');
  const opciones = document.querySelector(".opciones");
  const botonOpciones = opciones.querySelector("button");
  const checkboxs = document.querySelectorAll(".form-check .form-check-input");
  const inputBuscar = document.querySelector("#inputBusqueda");
  let sumaCheckbox = heightCheckbox(opciones.querySelectorAll(".form-check"));

  //evento de los checkboxs
  checkboxs.forEach((checkbox) => {
    checkbox.addEventListener("click", (e) => {
      if (!inputBuscar.value.trim()) {
        //si el input etsa vacio, no dejo que lo marque
        checkbox.checked = !checkbox.checked;
      }
      buscar(checkbox.getAttribute("id"), inputBuscar);
    })
  }
  );

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
      opciones.style.maxHeight = (sumaCheckbox+(sumaCheckbox*0.4))+"px"; //sumo el tamaño de cada checkbox mas un 40%
    }
    opciones.classList.toggle("activa");
  });
})