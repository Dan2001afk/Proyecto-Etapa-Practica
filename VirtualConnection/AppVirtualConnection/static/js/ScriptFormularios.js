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
    


