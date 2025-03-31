document.addEventListener("DOMContentLoaded", function () {
    const togglePassword = document.getElementById("togglePassword");
    const passwordField = document.getElementById("password");

    togglePassword.addEventListener("click", function () {
        if (passwordField.type === "password") {
            passwordField.type = "text";
            togglePassword.textContent = "🔓";
        } else {
            passwordField.type = "password";
            togglePassword.textContent = "🔒";
        }
    });
});
