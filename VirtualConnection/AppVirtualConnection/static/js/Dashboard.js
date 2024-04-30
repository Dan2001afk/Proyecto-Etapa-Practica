$(function () {
  var grid = GridStack.init();
          // Agrega el widget al gridstack
  grid.addWidget('<div><div class="grid-stack-item-content"><canvas id="myChart" width="400" height="200"></canvas></div></div>', {width: 4, height: 2});
  
  // Función para crear la gráfica
  function createChart() {
    const canvas = document.getElementById('myChart');
    const ctx = canvas.getContext('2d');
  
    const myChart = new Chart(ctx, {
      type: 'bar',
      data: {
        labels: ['Red', 'Blue', 'Yellow', 'Green', 'Purple', 'Orange'],
        datasets: [{
          label: '# of Votes',
          data: [12, 19, 3, 5, 2, 3],
          borderWidth: 1
        }]
      },
      options: {
        scales: {
          y: {
            beginAtZero: true
          }
        }
      }
    });
  
    return myChart;
  }
  
  let myChart = createChart(); // Crea la gráfica inicialmente
  
  // Actualiza la gráfica cuando cambia el tamaño del contenedor
  grid.on('resizestop', function(event, element) {
    if (myChart) {
      myChart.destroy(); // Destruye la instancia actual de la gráfica
    }
    
    myChart = createChart(); // Crea una nueva gráfica con el tamaño actualizado
  });
  
      });
  
  
  
  
  
      function generarGrafica() {
          const grid = GridStack.init();
          const label = document.getElementById('chart-label').value;
          const data = document.getElementById('chart-data').value.split(',').map(Number);
        
          // Validación básica de los datos
          if (!label || !data.every(value => !isNaN(value))) {
            alert('Por favor, ingresa una etiqueta y datos válidos para la gráfica.');
            return;
          }
        
          const canvasId = 'chartCanvas_' + Math.random().toString(36).substr(2, 9); // Genera un ID único para el canvas
          const canvasHTML = `<canvas id="${canvasId}" width="400" height="200"></canvas>`;
          const chartData = {
            labels: Array.from({ length: data.length }, (_, i) => 'Data ' + (i + 1)),
            datasets: [{
              label: label,
              data: data,
              borderWidth: 1
            }]
          };
        
          // Agrega el canvas al gridstack
          const gridElement = document.createElement('div');
          gridElement.classList.add('grid-stack-item-content');
          gridElement.innerHTML = canvasHTML;
          const gridWidget = grid.addWidget(gridElement, { width: 4, height: 2 });
        
          // Dibuja la gráfica en el canvas
          const ctx = document.getElementById(canvasId).getContext('2d');
          const chart = new Chart(ctx, {
            type: 'bar',
            data: chartData,
            options: {
              scales: {
                y: {
                  beginAtZero: true
                }
              }
            }
          });
        
          // Redibujar la gráfica cuando cambie el tamaño del widget de gridstack
          gridWidget.on('resizestop', function() {
            canvas.width = canvas.parentNode.clientWidth;
            canvas.height = canvas.parentNode.clientHeight;
            chart.resize();
          });
        
          // Limpia los campos del formulario
          document.getElementById('chart-label').value = '';
          document.getElementById('chart-data').value = '';
        }
        
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  // /*prueba con echarts js */
  // function PruebaEcharts() {
  // const grid = GridStack.init();
  // /*contenedor donde se va a generar la grafica*/ 
  // grid.addWidget('<div><div id="chartContainer" class="grid-stack-item-content"></div></div>', {width: 100, height: 200});
  
  // const chartContainer = document.getElementById('chartContainer');
  // const myChart = echarts.init(chartContainer);
  
  
  // const option = {
  //   //configuracion de la animacion de la grafica de libreria echarts
  
  //   series: [
  //     {
  //       type: 'gauge',
  //       center: ['50%', '60%'],
  //       startAngle: 200,
  //       endAngle: -20,
  //       min: 0,
  //       max: 60,
  //       splitNumber: 12,
  //       itemStyle: {
  //         color: '#FFAB91'
  //       },
  //       progress: {
  //         show: true,
  //         width: 30
  //       },
  //       pointer: {
  //         show: false
  //       },
  //       axisLine: {
  //         lineStyle: {
  //           width: 30
  //         }
  //       },
  //       axisTick: {
  //         distance: -45,
  //         splitNumber: 5,
  //         lineStyle: {
  //           width: 2,
  //           color: '#999'
  //         }
  //       },
  //       splitLine: {
  //         distance: -52,
  //         length: 14,
  //         lineStyle: {
  //           width: 3,
  //           color: '#999'
  //         }
  //       },
  //       axisLabel: {
  //         distance: -20,
  //         color: '#999',
  //         fontSize: 20
  //       },
  //       anchor: {
  //         show: false
  //       },
  //       title: {
  //         show: false
  //       },
  //       detail: {
  //         valueAnimation: true,
  //         width: '60%',
  //         lineHeight: 40,
  //         borderRadius: 8,
  //         offsetCenter: [0, '-15%'],
  //         fontSize: 60,
  //         fontWeight: 'bolder',
  //         formatter: '{value} °C',
  //         color: 'inherit'
  //       },
  //       data: [
  //         {
  //           value: 20
  //         }
  //       ]
  //     },
  //     {
  //       type: 'gauge',
  //       center: ['50%', '60%'],
  //       startAngle: 200,
  //       endAngle: -20,
  //       min: 0,
  //       max: 60,
  //       itemStyle: {
  //         color: '#FD7347'
  //       },
  //       progress: {
  //         show: true,
  //         width: 8
  //       },
  //       pointer: {
  //         show: false
  //       },
  //       axisLine: {
  //         show: false
  //       },
  //       axisTick: {
  //         show: false
  //       },
  //       splitLine: {
  //         show: false
  //       },
  //       axisLabel: {
  //         show: false
  //       },
  //       detail: {
  //         show: false
  //       },
  //       data: [
  //         {
  //           value: 20
  //         }
  //       ]
  //     }
  //   ]
  // };
  
  // myChart.setOption(option);
  
  // setInterval(function () {
  //   const random = +(Math.random() * 60).toFixed(2);
  //   myChart.setOption({
  //     series: [
  //       {
  //         data: [
  //           {
  //             value: random
  //           }
  //         ]
  //       },
  //       {
  //         data: [
  //           {
  //             value: random
  //           }
  //         ]
  //       }
  //     ]
  //   });
  // }, 2000);
  
  
  
  // }
  
  // PruebaEcharts();



//   function cargarDatosFirebase(params) {
//     const firebaseConfig = {
//         apiKey: "AIzaSyB_b0S3kj_ZVl0NSLp3NIWrD4uuEpjAihA",
//         authDomain: "virtualconnection-643e6.firebaseapp.com",
//         databaseURL: "https://virtualconnection-643e6-default-rtdb.firebaseio.com",
//         projectId: "virtualconnection-643e6",
//         storageBucket: "virtualconnection-643e6.appspot.com",
//         messagingSenderId: "1093478819923",
//         appId: "1:1093478819923:web:c0bf89d258396aba853ea6"
//       };

//     // Inicializar Firebase
//     firebase.initializeApp(firebaseConfig);
//     function obtenerDatosDelCultivo(cultivoId) {
//         const db = firebase.firestore();

//         // Referencia al documento específico del cultivo en Firestore
//         var cultivoRef = db.collection('Cultivos').doc(cultivoId);
//         console.log("La referencia a la base de datos es: " + cultivoRef.path);
//         // Obtener los datos del cultivo desde Firestore
//         cultivoRef.get().then(doc => {
//             if (doc.exists) {
//                 // Obtener los datos del documento
//                 const cultivoData = doc.data();
//                 console.log("Los datos del cultivo son: ", cultivoData);
//                 // Hacer algo con los datos del cultivo
//                 llenarFormulario(cultivoData);
//                 generarGraficas(cultivoData);
//             } else {
//                 console.error('No se encontró el documento del cultivo');
//             }
//         }).catch(error => {
//             console.error('Error al obtener datos del cultivo:', error);
//         });
//     }


//     // Función para llenar el formulario con los datos del cultivo
//     function llenarFormulario(cultivoData) {
//         // Aquí llenarías el formulario con los datos del cultivo
//         // Por ejemplo:
//         console.log("estos son los datos que se están almacenando en la variable" + cultivoData)
//         document.getElementById('nombre').value = cultivoData.nombre;
//         document.getElementById('ubicacion').value = cultivoData.ubicacion;
//         document.getElementById('variedad').value = cultivoData.variedad;
//         document.getElementById('Temperatura_suelo').value = cultivoData.Temperatura_suelo;
//         document.getElementById('Humedad').value = cultivoData.Humedad;
//     }

//     // Luego, cuando se hace clic en el botón "Generar Formulario"
//     document.querySelectorAll('.boton').forEach(button => {
//         button.addEventListener('click', function () {
//             const cultivoId = this.getAttribute('data-cultivo-id');
//             // Llamamos a la función para obtener los datos del cultivo
//             obtenerDatosDelCultivo(cultivoId);
//         });
//     });
// }
// cargarDatosFirebase();


// function generarGraficas(cultivoData) {
//     const etiquetas = ['Temperatura del suelo', 'Humedad'];
//     const datos = [cultivoData.Temperatura_suelo, cultivoData.Humedad];

//     const ctx = document.getElementById('miGrafico').getContext('2d');

//     const miGrafico = new Chart(ctx, {
//         type: 'bar', // Tipo de gráfico (barra en este caso)
//         data: {
//           labels: etiquetas, // Etiquetas para el eje X
//           datasets: [{
//             label: 'Datos del Cultivo', // Etiqueta para la leyenda
//             data: datos, // Datos para el eje Y
//             backgroundColor: 'rgba(255, 99, 132, 0.2)', // Color de fondo de las barras
//             borderColor: 'rgba(255, 99, 132, 1)', // Color del borde de las barras
//             borderWidth: 1 // Ancho del borde de las barras
//           }]
//         },
//         options: {
//           scales: {
//             y: {
//               beginAtZero: true // Comenzar el eje Y en cero
//             }
//           }
//         }
//       });     
// }

// generarGraficas();