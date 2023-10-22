function togglePasswordVisibility() {
    const passwordInput = document.getElementById("userPassword");
    const togglePasswordButton = document.getElementById("togglePassword");
  
    if (passwordInput.type === "password") {
      passwordInput.type = "text";
      togglePasswordButton.innerHTML = '<i class="bi bi-eye-slash"></i>'; // Show the eye icon
    } else {
      passwordInput.type = "password";
      togglePasswordButton.innerHTML = '<i class="bi bi-eye"></i>'; // Hide the eye icon
    }
  }
  