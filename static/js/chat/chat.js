
  //obtener el script
  const scriptElement = document.currentScript;

  //obtengo los valores de data
  const username = scriptElement.getAttribute("data-username");
  const chat = scriptElement.getAttribute("data-chat");

  // Web sockect
  var ws_scheme = window.location.protocol == "https:" ? "wss" : "ws";

  var chatSocket = new ReconnectingWebSocket(
    ws_scheme + "://" + window.location.host + `/ws/chat/${chat}/`
  );

  // Obtener referencia al contenedor de mensajes del chat
  var chatMessages = document.querySelector(".chat-messages");
  chatMessages.scrollTop = chatMessages.scrollHeight;
  // Agregar un evento de mensaje recibido al WebSocket
  chatSocket.onmessage = function (e) {
    var data = JSON.parse(e.data);
    var message = data["message"];
    var user = null;
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
    var messageElement = document.createElement("div");
    messageElement.classList.add("message");
    if (user == username) {
      messageElement.innerHTML = `<div class="local" style="margin-left:auto;">
            <div class="d-flex flex-column">
              <span class="align-self-end t-wordwrap">${message}</span>
              <small class="align-self-end">${timeFormat}</small>
            </div>
          </div>`;
    } else {
      let usernameMensaje=username;
      try {
        usernameMensaje = toTitle(user);
      } catch (e) {
        usernameMensaje = username;
      }
      messageElement.innerHTML = `<div class="no-local" style="margin-right:auto;">
            <strong style="display:block;">${usernameMensaje}</strong>
            <div class="d-flex flex-column">
              <span class="align-self-start t-wordwrap">${message}</span>
              <small>${timeFormat}</small>
            </div>
          </div>`;
    }

    chatMessages.appendChild(messageElement);

    // Desplazarse hacia abajo para mostrar el mensaje más reciente
    chatMessages.scrollTop = chatMessages.scrollHeight;
  };
  // Obtener referencias a los elementos del chat
  var chatInput = document.querySelector(".chat-input input");
  var sendButton = document.querySelector(".chat-input button");

  // Agregar un evento de clic al botón de enviar
  sendButton.addEventListener("click", function () {
    var message = chatInput.value.trim();
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
  chatInput.addEventListener("keypress", function (event) {
    if (event.keyCode === 13 || event.which === 13) {
      // Obtener el mensaje del campo de entrada
      var message = chatInput.value.trim();
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

