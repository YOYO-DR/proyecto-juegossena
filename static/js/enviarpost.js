function enviarPost(idForm, csrftoken, url, funcion) {
  const form = document.getElementById(idForm);

  form.addEventListener("submit", async (e) => {
    e.preventDefault();
    //obtengo el boton del formulario
    const btnSubmit = form.querySelector('button[type="submit"]');
    //obtengo el valor inicial del boton
    let valorSubmit = btnSubmit.innerHTML;
    //creo el spiner de bootstrap
    let spanLoading = `<div class="ms-1 spinner-border spinner-border-sm" role="status">
  <span class="visually-hidden">Loading...</span>
</div>`;
    //Agrego el valor del boton mas el spinner
    btnSubmit.innerHTML = `${valorSubmit}${spanLoading}`
    //deshabilito el boton
    btnSubmit.disabled=true
    const formData = new FormData(form);

    try {
      const response = await fetch(url, {
        method: "POST",
        headers: {
          "X-CSRFToken": csrftoken,
        },
        body: formData,
      });
      const data = await response.json();
      if (response.ok) {
        form.reset();
      }
      funcion(data); //ejecutar funcion si la respuesta es correcta
    } catch (error) {
      console.error("Error:", error);
    }
    //habilito el boton
    btnSubmit.disabled = false
    //dejo ahora solo el valor del botón
    btnSubmit.innerHTML=`${valorSubmit}`
  });
}
