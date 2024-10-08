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

cargarDatosFirebase();

// Función para generar la gráfica en un canvas específico
function generarGraficaEnCanvas(canvas, cultivoData) {
    var ctx = canvas.getContext('2d');
    const nombre_cultivo = cultivoData.nombre;
    
    /* Variables para mostrar hora y fecha */
    const ahora = new Date();
    const fecha = ahora.toLocaleDateString();
    const hora = ahora.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    
    var myChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: ['Temperatura del suelo', 'Humedad'], 
            datasets: [{
                label: `${nombre_cultivo}`, 
                data: [0, 0], 
                backgroundColor: [
                    'rgba(255, 99, 132, 0.2)',
                    'rgba(54, 162, 235, 0.2)'  
                ],
                borderColor: [
                    'rgba(255, 99, 132, 1)',   
                    'rgba(54, 162, 235, 1)'    
                ],
                borderWidth: 1 
            }]
        },
        options: {
            plugins: {
                legend: {
                    position: 'top',
                },
                title: {
                    display: true,
                    text: `${fecha} - ${hora}`
                },
                subtitle: {
                    display: true,
                    text: '',
                    color: 'gray',
                    font: {
                        size: 14,
                        family: 'calibri',
                        weight: 'normal',
                    },
                    padding: {
                        bottom: 10
                    }
                }
            },
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });

    function actualizarDatos() {
        // Ruta del archivo JSON basado en el nombre del cultivo
        const url = `/static/json/${nombre_cultivo}.json`; 
    
        fetch(url)
            .then(response => {
                if (!response.ok) {
                    throw new Error('Archivo JSON no encontrado');
                }
                return response.json();
            })
            .then(data => {
                // Supongamos que el JSON tiene un formato como [{ temperatura: X, humedad: Y }]
                const ultimoReporte = data[data.length - 1]; // Obtener el último reporte
    
                const temperatura = ultimoReporte.temperatura;
                const humedad = ultimoReporte.humedad;
    
                // Actualizar los datos en la gráfica
                myChart.data.datasets[0].data[0] = temperatura; // Temperatura
                myChart.data.datasets[0].data[1] = humedad;     // Humedad
    
                myChart.options.plugins.subtitle.text = `Temperatura actual: ${temperatura}°C, Humedad actual: ${humedad}%`;
    
                myChart.update();
            })
            .catch(error => {
                console.error('Error al cargar el JSON:', error);
            });
    }
    
    // Cargar los datos inmediatamente al generar la gráfica
    actualizarDatos();
    
    // Actualizar los datos cada intervalo definido en la variable de entorno
    setInterval(actualizarDatos, INTERVALO_ACTUALIZACION_GRAFICA);

    return myChart;
}


function crearGrafica(cultivoData, grid) {
    var options = { width: 10, height: 10 }; // Opciones de tamaño para el widget de GridStack
    var content = '<div class="grid-stack-item-content"><canvas class="grafica-canvas" width="400" height="200"></canvas></div>'; // Contenido HTML del widget
    var widget = grid.addWidget(content, options); // Agregar el widget al GridStack
    var canvas = widget.querySelector('.grafica-canvas'); // Seleccionar el canvas dentro del widget
    generarGraficaEnCanvas(canvas, cultivoData); // Generar la gráfica en el canvas seleccionado con los datos del cultivo

}

function simularLecturaTemperatura() {
    return (Math.random() * (30 - 15) + 15).toFixed(2);
}

function simularLecturaHumedad() {
    return (Math.random() * (80 - 40) + 40).toFixed(2);
}

document.addEventListener("DOMContentLoaded", function() {
    // Obtener temperatura y humedad utilizando las funciones de simulación
    var temperatura = simularLecturaTemperatura();
    var humedad = simularLecturaHumedad();

    // Asignar los valores a los campos del formulario
    document.getElementById("id_temperatura_suelo").value = temperatura;
    document.getElementById("id_humedad").value = humedad;
});


// Función para crear un JSON con los datos y enviarlos al servidor
function guardarJSON(cultivoNombre) {
    const timestamp = new Date().toISOString();
    const datos = {
        cultivo: cultivoNombre,
        temperatura: simularLecturaTemperatura(),
        humedad: simularLecturaHumedad(),
        timestamp: timestamp
    };

    fetch('/guardar-json/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': obtenerCSRFToken(), // Si usas CSRF token en Django
        },
        body: JSON.stringify(datos),
    })
    .then((response) => {
        if (!response.ok) {
            throw new Error('Error al guardar el JSON');
        }
        return response.json();
    })
    .then((data) => {
        console.log('JSON guardado correctamente:', data);
    })
    .catch((error) => {
        console.error('Error:', error);
    });
}

function iniciarGeneracionReportes(cultivoNombre) {
    let contador = 0;

    // Generar el primer reporte inmediatamente
    guardarJSON(cultivoNombre);
    contador++;

    // Iniciar el intervalo para los siguientes reportes
    const interval = setInterval(() => {
        if (contador < 500000) {
            guardarJSON(cultivoNombre);
            contador++;
        } else {
            clearInterval(interval);
            console.log('Generación de reportes finalizada para:', cultivoNombre);
        }
    }, INTERVALO_GENERACION_REPORTES); // Usar variable de entorno
}

  
  // Función para obtener el CSRF Token desde las cookies (necesaria si tu vista en Django está protegida por CSRF)
  function obtenerCSRFToken() {
    const name = 'csrftoken';
    const cookieValue = document.cookie
      .split('; ')
      .find((row) => row.startsWith(name))
      ?.split('=')[1];
    return cookieValue || '';
}


// Vincula la función guardarJSON() al evento click del botón
// document.getElementById('boton-json').addEventListener('click', guardarJSON);

document.querySelectorAll('.boton').forEach((boton) => {
    boton.addEventListener('click', () => {
        // Agregar la clase 'hidden' para iniciar la animación
        boton.classList.add('hidden'); 
        
        // Obtén el nombre del cultivo desde el atributo 'data-cultivo-nombre'
        const cultivoNombre = boton.getAttribute('data-cultivo-nombre'); // Cambia esto si usas ID
        iniciarGeneracionReportes(cultivoNombre); // Iniciar la generación de reportes
        console.log(cultivoNombre); // Para verificar el nombre del cultivo
    });
});

















/*ACTUALIZAR CULTIVOS*/


document.getElementById('formActualizarCultivo').addEventListener('submit', function(event) {
    event.preventDefault();  // Evitar el envío normal del formulario

    const formData = new FormData(this);  // Obtener los datos del formulario

    fetch(this.action, {
        method: 'POST',
        body: formData,
        headers: {
            'X-CSRFToken': '{{ csrf_token }}'  // Asegúrate de incluir el token CSRF
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert('Cultivo actualizado con éxito');
            location.reload(); // Recargar la página para ver los cambios
        } else {
            alert('Error al actualizar el cultivo: ' + data.error);
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Ocurrió un error al actualizar el cultivo.');
    });
});












/*ELIMINAR CULTIVOS*/



function eliminarCultivo(cultivoId) {
    if (confirm("¿Estás seguro de que quieres eliminar este cultivo?")) {
        const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');  // Obtener el token CSRF
        
        fetch(`/cultivos/eliminar/${cultivoId}/`, {
            method: 'DELETE',
            headers: {
                'X-CSRFToken': csrfToken  // Incluir el token CSRF
            }
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Error al eliminar el cultivo');
            }
            return response.json();
        })
        .then(data => {
            if (data.success) {
                alert('Cultivo eliminado con éxito');
                location.reload();  // Recarga la página para ver los cambios
            } else {
                alert('Error al eliminar el cultivo: ' + data.error);
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Ocurrió un error al eliminar el cultivo.');
        });
    }
}

















