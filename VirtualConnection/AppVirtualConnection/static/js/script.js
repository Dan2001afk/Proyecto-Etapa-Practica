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



let grid;

function cargarDatosFirebase(params) {
    grid = GridStack.init();
    const firebaseConfig = {
        apiKey: "AIzaSyB_b0S3kj_ZVl0NSLp3NIWrD4uuEpjAihA",
        authDomain: "virtualconnection-643e6.firebaseapp.com",
        databaseURL: "https://virtualconnection-643e6-default-rtdb.firebaseio.com",
        projectId: "virtualconnection-643e6",
        storageBucket: "virtualconnection-643e6.appspot.com",
        messagingSenderId: "1093478819923",
        appId: "1:1093478819923:web:c0bf89d258396aba853ea6"
    };

    // Inicializar Firebase
    firebase.initializeApp(firebaseConfig);

    function obtenerDatosDelCultivo(cultivoId) {
        return new Promise((resolve, reject) => {
            const db = firebase.firestore();

            // Referencia al documento específico del cultivo en Firestore
            var cultivoRef = db.collection('Cultivos').doc(cultivoId);

            // Obtener los datos del cultivo desde Firestore
            cultivoRef.get().then(doc => {
                if (doc.exists) {
                    // Si el documento existe, resolver la promesa con los datos del cultivo
                    const cultivoData = doc.data();
                    resolve(cultivoData);
                } else {
                    // Si el documento no existe, rechazar la promesa con un mensaje de error
                    reject('No se encontró el documento del cultivo');
                }
            }).catch(error => {
                // Si hay un error al obtener los datos, rechazar la promesa con el error
                reject('Error al obtener datos del cultivo:', error);
            });
        });
    }

    document.querySelectorAll('.boton').forEach(button => {
        button.addEventListener('click', function () {
            const cultivoId = this.getAttribute('data-cultivo-id');
            // Llamamos a la función para obtener los datos del cultivo
            obtenerDatosDelCultivo(cultivoId)
                .then(cultivoData => crearGrafica(cultivoData, grid)) // Pasar grid como argumento
                .catch(error => console.error(error));
        });
    });
    
}


function crearGrafica(cultivoData, grid) {
    var options = { width: 10, height: 10 }; // Opciones de tamaño para el widget de GridStack
    var content = '<div class="grid-stack-item-content"><canvas class="grafica-canvas" width="400" height="200"></canvas></div>'; // Contenido HTML del widget
    var widget = grid.addWidget(content, options); // Agregar el widget al GridStack
    var canvas = widget.querySelector('.grafica-canvas'); // Seleccionar el canvas dentro del widget
    generarGraficaEnCanvas(canvas, cultivoData); // Generar la gráfica en el canvas seleccionado con los datos del cultivo
    
}

cargarDatosFirebase();

// Función para generar la gráfica en un canvas específico
function generarGraficaEnCanvas(canvas, cultivoData) {
    var ctx = canvas.getContext('2d');
    // Usar los datos del cultivo para generar la gráfica
    var myChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: ['Temperatura del suelo', 'Humedad'], // Etiquetas para el eje X
            datasets: [{
                label: 'Datos del Cultivo', // Etiqueta para la leyenda
                data: [cultivoData.Temperatura_suelo, cultivoData.Humedad], // Datos para el eje Y
                backgroundColor: 'rgba(255, 99, 132, 0.2)', // Color de fondo de las barras
                borderColor: 'rgba(255, 99, 132, 1)', // Color del borde de las barras
                borderWidth: 1 // Ancho del borde de las barras
            }]
        },
        options: {
            scales: {
                y: {
                    beginAtZero: true // Comenzar el eje Y en cero
                }
            }
        }
    });

    
    document.addEventListener('DOMContentLoaded', function () {
        grid.on('resizestop', function (event, el) {
            // Obtener el canvas dentro del widget
            var canvas = el.querySelector('.grafica-canvas');
            // Ajustar el tamaño del canvas para que coincida con el nuevo tamaño del contenedor
            canvas.width = canvas.parentNode.clientWidth;
            canvas.height = canvas.parentNode.clientHeight;
            // Si estás utilizando Chart.js para la gráfica, redimensionar la gráfica
            if (chart) {
                chart.resize();
            }
        });
    });
}



