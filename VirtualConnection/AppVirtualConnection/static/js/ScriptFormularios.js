    document.getElementById('sign-up').addEventListener('click', function() {
        // Redirecciona a la página deseada
        window.location.href = '/RegistrarUsuarios';
    });





    /*Visualizar Contraseña cuando se digita en el formulario de iniciar sesion*/
    document.addEventListener('DOMContentLoaded', function() {
        var togglePassword = document.getElementById('togglePassword');
        var passwordField = document.getElementById('password');
        
        togglePassword.addEventListener('click', function() {
            var type = passwordField.getAttribute('type') === 'password' ? 'text' : 'password';
            passwordField.setAttribute('type', type);
            togglePassword.textContent = type === 'password' ? 'Mostrar contraseña' : 'Ocultar contraseña';
        });
    });
    



function abrirModal() {
    document.getElementById('modalActualizarCultivo').style.display = 'block';
}

function cerrarModal() {
    document.getElementById('modalActualizarCultivo').style.display = 'none';
}


function cargarDatosCultivo(id, nombre, ubicacion, variedad, temperatura_suelo, humedad) {
    // Establecer el valor de los campos del formulario
    document.getElementById('nombre').value = nombre;
    document.getElementById('ubicacion').value = ubicacion;
    document.getElementById('variedad').value = variedad;
    document.getElementById('temperatura_suelo').value = temperatura_suelo; // Cargar temperatura
    document.getElementById('humedad').value = humedad; // Cargar humedad

    // Configurar la acción del formulario para que apunte a la URL de actualización
    document.getElementById('formActualizarCultivo').action = '/cultivos/actualizar/' + id + '/';
    // Abrir el modal
    abrirModal();
}


