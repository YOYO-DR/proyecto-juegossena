  //obtener el script
  const scriptElement = document.currentScript,

  //obtengo los valores de data
  username = scriptElement.getAttribute("data-username"),
  chat = scriptElement.getAttribute("data-chat"),

  //constantes
  chatInput = document.querySelector(".chat-input input"),
  sendButton = document.querySelector(".chat-input button");

  // Web sockect
  let ws_scheme = window.location.protocol == "https:" ? "wss" : "ws";

  let chatSocket = new ReconnectingWebSocket(
    ws_scheme + "://" + window.location.host + `/ws/chat/${chat}/`
);

//cuando se conecta el socket
chatSocket.addEventListener("open", (e) => {
  //activo el boton y el input apenas se conecte
  chatInput.placeholder = "Escribe un mensaje...";
  chatInput.disabled = false;
  sendButton.disabled = false;
})

//por si se desconecta del socket
chatSocket.addEventListener("close", (e) => {
  chatInput.placeholder = "Conectando...";
  chatInput.disabled = true;
  sendButton.disabled = true;
 })

  // Obtener referencia al contenedor de mensajes del chat
  let chatMessages = document.querySelector(".chat-messages");
  chatMessages.scrollTop = chatMessages.scrollHeight;
  // Agregar un evento de mensaje recibido al WebSocket
  chatSocket.onmessage = function (e) {
    let data = JSON.parse(e.data);
    let message = data["message"];
    let user = null;
    try {
      user = data["user"];
    } catch (e) {
      console.error(e);
      user = null;
    }
    if (user == null) {
      user = "Anonimo";
    }

    //obtengo el datetime actual
    const c = new Date(); // Obtiene la fecha y hora actual

    //formateo la fecha para que salga como "2:25 PM"
    let hours = c.getHours();
    let minutes = c.getMinutes();
    let ampm = hours >= 12 ? "PM" : "AM";

    hours = hours % 12;
    hours = hours ? hours : 12; // la hora '0' debería ser '12'
    minutes = minutes < 10 ? "0" + minutes : minutes;

    let timeFormat = hours + ":" + minutes + " " + ampm;

    // Crear un elemento de mensaje y agregarlo al contenedor de mensajes
    let messageElement = document.createElement("div");
    messageElement.classList.add("message");
    if (user == username) {
      messageElement.textContent=''
      messageElement.insertAdjacentHTML(
        "afterbegin",
        `<div class="local" style="margin-left:auto;">
            <div class="d-flex flex-column">
              <span class="align-self-end t-wordwrap">${message}</span>
              <small class="align-self-end">${timeFormat}</small>
            </div>
          </div>`
      );
    } else {
      let usernameMensaje=username;
      try {
        usernameMensaje = F.toTitle(user);
      } catch (e) {
        usernameMensaje = username;
      }
      messageElement.textContent=""
      messageElement.insertAdjacentHTML(
        "afterbegin",
        `<div class="no-local" style="margin-right:auto;">
            <strong style="display:block;">${usernameMensaje}</strong>
            <div class="d-flex flex-column">
              <span class="align-self-start t-wordwrap">${message}</span>
              <small>${timeFormat}</small>
            </div>
          </div>`
      );
    }

    chatMessages.appendChild(messageElement);

    // Desplazarse hacia abajo para mostrar el mensaje más reciente
    chatMessages.scrollTop = chatMessages.scrollHeight;
};
  
  // Agregar un evento de clic al botón de enviar
  sendButton.addEventListener("click", function () {
    let message = chatInput.value.trim();
    if (message !== "") {
      // Enviar el mensaje al WebSocket
      chatSocket.send(
        JSON.stringify({
          message: message,
          user: username,
        })
      );

      // Limpiar el campo de entrada del chat
      chatInput.value = "";
    }
  });

  // Agregar un evento de tecla presionada al campo de entrada del chat (Cuando le una enter)
  chatInput.addEventListener("keydown", function (event) {
    if (event.key === "Enter") {
      // Obtener el mensaje del campo de entrada
      let message = chatInput.value.trim();
      if (message !== "") {
        // Enviar el mensaje al WebSocket
        chatSocket.send(
          JSON.stringify({
            message: message,
            user: username,
          })
        );

        // Limpiar el campo de entrada del chat
        chatInput.value = "";
      }
    }
  });

