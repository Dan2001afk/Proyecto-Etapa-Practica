const body = document.querySelector("body"),
    sidebar = body.querySelector(".sidebar"),
    toggle = body.querySelector(".toggle"),
    SearchBtn = body.querySelector(".search-box"),
    modelSwitch = body.querySelector(".toggle-switch"),
    modeText = body.querySelector(".mode-text");

// Obtén el estado del menú lateral desde el almacenamiento de sesión
const getSidebarState = () => sessionStorage.getItem('sidebarState') === 'true';

// Establece el estado del menú lateral en el almacenamiento de sesión
const setSidebarState = (state) => sessionStorage.setItem('sidebarState', state);

// Aplica el estado del menú lateral
const applySidebarState = () => {
    if (getSidebarState()) {
        sidebar.classList.add("close");
    } else {
        sidebar.classList.remove("close");
    }
};

applySidebarState(); // Aplica el estado del menú lateral al cargar la página

toggle.addEventListener("click", () => {
    sidebar.classList.toggle("close");
    setSidebarState(sidebar.classList.contains("close"));
});

SearchBtn.addEventListener("click", () => {
    sidebar.classList.remove("close");
    setSidebarState(false);
});

modelSwitch.addEventListener("click", () => {
    body.classList.toggle("dark");

    if (body.classList.contains("dark")) {
        modeText.innerText = "ligth mode"
    } else {
        modeText.innerText = "Dark mode"
    }
});








firebase.auth().onAuthStateChanged(function(user) {
    if (user) {
      var displayName = user.displayName; // Obtén el nombre de usuario
      enviarNombreUsuario(displayName); // Llama a la función para enviar el nombre de usuario
    } else {
      // El usuario no está autenticado.
    }
  });
  
  function enviarNombreUsuario(username) {
    fetch('/ruta/en/django/para/mi/vista', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
      },
      body: 'username=' + encodeURIComponent(username),
    })
    .then(response => {
      if (response.ok) {
        console.log('Nombre de usuario enviado correctamente a Django');
      } else {
        console.error('Error al enviar el nombre de usuario a Django');
      }
    })
    .catch(error => {
      console.error('Error:', error);
    });
  }
  