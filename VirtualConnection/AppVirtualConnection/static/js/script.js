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



/*redireccionar al dar click en el boton del formulario generar graficas*/
function redireccionar(params) {
    //     document.getElementById("boton").addEventListener("click", function() {
    //         // Acción a realizar al hacer clic en el botón, por ejemplo, redirigir a otra página
    //         window.location.href = "Dashboard";
    //       });
    document.querySelectorAll('#boton').forEach(button => {
        button.addEventListener('click', function () {
            window.location.href = "Dashboard";
        });
    });
}

redireccionar();


function cargarDatosFirebase(params) {

   
    // Obtener una referencia a la base de datos de Firebase
    var firestore = firebase.firestore();
    // Función para obtener los datos del cultivo
    function obtenerDatosDelCultivo(cultivoId) {
        // Referencia al documento específico del cultivo en Firestore
        var cultivoRef = firestore.collection('Cultivos').doc(cultivoId);
        console.log("La referencia a la base de datos es: " + cultivoRef.path);
        // Obtener los datos del cultivo desde Firestore
        cultivoRef.get().then(doc => {
            if (doc.exists) {
                // Obtener los datos del documento
                const cultivoData = doc.data();
                console.log("Los datos del cultivo son: ", cultivoData);
                // Hacer algo con los datos del cultivo
                llenarFormulario(cultivoData);
            } else {
                console.error('No se encontró el documento del cultivo');
            }
        }).catch(error => {
            console.error('Error al obtener datos del cultivo:', error);
        });
    }
    

    // Función para llenar el formulario con los datos del cultivo
    function llenarFormulario(cultivoData) {
        // Aquí llenarías el formulario con los datos del cultivo
        // Por ejemplo:
        console.log("estos son los datos que se están almacenando en la variable" + cultivoData)
        document.getElementById('nombre').value = cultivoData.nombre;
        document.getElementById('ubicacion').value = cultivoData.ubicacion;
        document.getElementById('variedad').value = cultivoData.variedad;
        document.getElementById('Temperatura_suelo').value = cultivoData.Temperatura_suelo;
        document.getElementById('Humedad').value = cultivoData.Humedad;
    }

    // Luego, cuando se hace clic en el botón "Generar Formulario"
    document.querySelectorAll('.boton').forEach(button => {
        button.addEventListener('click', function () {
            const cultivoId = this.getAttribute('data-cultivo-id');
            // Llamamos a la función para obtener los datos del cultivo
            obtenerDatosDelCultivo(cultivoId);
        });
    });
}



cargarDatosFirebase();