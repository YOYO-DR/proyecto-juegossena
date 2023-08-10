//activar - desactivar botones
function disabledBotones(botones) {
  botones.forEach((boton) => {
    boton.disabled = !boton.disabled
  })
}

//enviar peticion
function peticionPost(url,csrf_token,data,funcion,final) {
  fetch(window.location.pathname, {
    method: "POST",
    headers: {
      "X-CSRFToken": csrf_token,
    },
    body: JSON.stringify(data),
  })
    .then((response) => {
      if (!response.ok) {
        throw new Error("Network response was not ok");
      }
      return response.json();
    })
    .then((data) => {
      funcion(data);
    })
    .catch((error) => {
      // Maneja cualquier error ocurrido durante la petición
      console.error("Fetch error:", error);
    }).finally(() => { 
      final()
    });
}


function dispoModal(
  botonesModalDispo,
  botonesEliminarDispo,
  modalDispo,
  modalTitulo,
  modalBody,
  csrf_token
) {
  botonesModalDispo.forEach((boton) => {
    //activar los botones
    boton.disabled = false;
    boton.addEventListener("click", function (e) {
      e.preventDefault();

      //obtengo el valor inicial del boton
      let valorBoton = boton.innerHTML;
      //creo el spiner de bootstrap
      let spanLoading = `<div class="ms-1 spinner-border spinner-border-sm" role="status">
          <span class="visually-hidden">Loading...</span>
        </div>`;
      boton.innerHTML = `${valorBoton}${spanLoading}`;
      disabledBotones(botonesModalDispo);
      let idDispo = 0;
      let clasesBoton = boton.className.split(" ");
      clasesBoton.forEach((element) => {
        if (element.includes("modalDispo")) {
          idDispo = element.replace("modalDispo", "");
        }
      });

      //con el id del dispositivo mando una petición con fetch para obtener la información del boton
      // Crea una nueva instancia del modal
      let modal = new bootstrap.Modal(modalDispo);
      //Aqui pongo los valores del dispositivo en el formulario
      //hago una peticion post a la vista
      peticionPost(
        window.location.pathname,
        csrf_token,
        { id: idDispo, action: "datosDispo" },
        (data) => {
          // Trabaja con los datos obtenidos de la respuesta
          //console.log(data);
          if (data.dispositivo) {
            let dispo = data.dispositivo;
            modalTitulo.innerHTML = dispo.nombre;
            //acomodo lista de graficas
            let graficas = ``;
            if (dispo.grafica.length > 1) {
              graficas = `<p><b>Graficas:</b></p>`;
              graficas += `<ul>`;
              for (let i = 0; i < dispo.grafica.length; i++) {
                graficas += `<li><b>${i + 1}:</b> ${dispo.grafica[i].nombre}`;
                if (dispo.grafica[i].gb != null && dispo.grafica[i].gb > 0) {
                  graficas += ` - ${dispo.grafica[i].gb} GB`;
                }
                graficas += `</li>`;
              }
              graficas += `</ul>`;
            } else {
              graficas = `<p><b>Grafica:</b> ${dispo.grafica[0].nombre}`;
              if (dispo.grafica[0].gb != null && dispo.grafica[0].gb > 0) {
                graficas += ` - ${dispo.grafica[0].gb} GB`;
              }
              graficas += `</p>`;
            }
            //procesador
            let procesador = `<p><b>Procesador:</b> ${dispo.procesador.nombre}</p>`;
            //ram
            let rams = ``;
            if (dispo.ram.length > 1) {
              rams = `<p><b>Rams:</b></p>`;
              for (let i = 0; i < dispo.ram.length; i++) {
                rams += `<li><b>${i + 1}:</b> ${dispo.ram[i].gb}GB ${
                  dispo.ram[i].tipo
                } `;
                if (dispo.ram[i].velocidad) {
                  rams += `${dispo.ram[i].velocidad} Mhz`;
                }
                rams += `</li>`;
              }
              rams += `</ul>`;
            } else {
              rams = `<p><b>Ram:</b> ${dispo.ram[0].gb}GB ${dispo.ram[0].tipo}`;
              if (dispo.ram[0].velocidad) {
                rams += ` ${dispo.ram[0].velocidad} Mhz`;
              }
              rams += `</p>`;
            }

            //genero el modal
            let divModal = `<div>
            <p><b>Sistema operativo:</b> ${dispo.sistemaOperativo}</p>
            ${procesador}
            <p><b>Espacio:</b> ${dispo.espacioGb} GB</p>
            ${graficas}
            ${rams}

          </div>`;
            //lo muestro
            modalBody.innerHTML = divModal;
            modal.show();
          } else {
            alert(data.error);
          }
        },
        () => {
          //quito el spinner del boton
          disabledBotones(botonesModalDispo);
          boton.innerHTML = valorBoton;
        }
      );

    });
  });
  botonesEliminarDispo.forEach((boton) => {
    //activar los botones
    boton.disabled = false;
    boton.addEventListener("click", function (e) {
      e.preventDefault();
      //obtengo el valor inicial del boton
      let valorBoton = boton.innerHTML;
      //creo el spiner de bootstrap
      let spanLoading = `<div class="ms-1 spinner-border spinner-border-sm" role="status">
          <span class="visually-hidden">Loading...</span>
        </div>`;
      boton.innerHTML = `${valorBoton}${spanLoading}`;
      disabledBotones(botonesEliminarDispo);
      let idDispo = 0;
      let clasesBoton = boton.className.split(" ");
      clasesBoton.forEach((element) => {
        if (element.includes("eliminarDispo")) {
          idDispo = element.replace("eliminarDispo", "");
        }
      });

      peticionPost(window.location.pathname,
        csrf_token,
        {id:idDispo,action:"eliminar"},
        (data) => {
          if (data.eliminacion) {
            const contenedor = document.querySelector(".contenedorDispo");
            const divDispo = contenedor.querySelector(`.dispoCont${idDispo}`);
            contenedor.removeChild(divDispo)
            let divDispoCount = contenedor.querySelectorAll('[class*="dispoCont"]').length;
            console.log(divDispoCount);
            if (divDispoCount == 0) {
              let h2 = document.createElement("h2");
              h2.innerHTML="Sin dispositivos"
              contenedor.appendChild(h2)
              const tituloH1 = document.getElementById("tituloH1");
              tituloH1.innerHTML="Dispositivos"
            } else {
              const tituloH1 = document.getElementById("tituloH1");
              tituloH1.innerHTML = `Dispositivos ${divDispoCount}`;
            }
          }
        },
        () => {
          disabledBotones(botonesEliminarDispo);
          boton.innerHTML = valorBoton
        });
      
    });
  });
}