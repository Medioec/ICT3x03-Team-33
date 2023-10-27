// Add an event listener to handle the click event
document.getElementById("togglePassword").addEventListener("click", togglePasswordVisibility);

function togglePasswordVisibility() {
  const passwordInput = document.getElementById("userPassword");
  const togglePasswordButton = document.getElementById("togglePassword");

  if (passwordInput.type === "password") {
    passwordInput.type = "text";
    togglePasswordButton.querySelector("i").className = "bi bi-eye-slash"; // Show the eye icon
  } else {
    passwordInput.type = "password";
    togglePasswordButton.querySelector("i").className = "bi bi-eye"; // Hide the eye icon
  }
}
