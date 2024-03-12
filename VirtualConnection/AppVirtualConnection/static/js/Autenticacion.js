function validateForm() {
   var email = document.getElementById("email").value;
   var password = document.getElementById("password").value;
   var error_message = "";

   if (email === "") {
       error_message += "El campo de correo electrónico es obligatorio. ";
   }

   if (password === "") {
       error_message += "El campo de contraseña es obligatorio.";
   }

   if (error_message !== "") {
       document.getElementById("error").innerHTML = error_message;
       return false; // Impide el envío del formulario si hay errores.
   }

   return true; // Envía el formulario si no hay errores.
}