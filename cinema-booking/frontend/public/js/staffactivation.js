// Define a function to check if all registration fields and the form are valid
function checkRegistrationFields() {
    const $userPasswordInput = $("#userPassword");
    const isFormValid = $("#register-form").valid(); // Check overall form validity
  
    // Sanitize input values using DOMPurify
    const password = DOMPurify.sanitize($userPasswordInput.val());
  
    // Return true if all fields are filled correctly and the form is valid
    return email && username && password && isFormValid;
  }
  
  // Define the onSuccess function to handle the captcha callback
  function onSuccess() {
    const $registerButton = $("#register-button");
    if (checkRegistrationFields() && grecaptcha.getResponse()) {
      $registerButton.prop("disabled", false);
    } else {
      $registerButton.prop("disabled", true);
    }
  }
  
  document.addEventListener("DOMContentLoaded", function () {
    const $registerButton = $("#register-button");
    const $userPasswordInput = $("#userPassword");
  
    $userPasswordInput.on("input", function () {
      if (checkRegistrationFields()) {
        onSuccess(); 
      } else {
        $("#register-button").prop("disabled", true);
      }
    });
  
    $registerButton.click(async function (event) {
      event.preventDefault();
  
      if ($("#register-form").valid()) {
        const password = DOMPurify.sanitize($userPasswordInput.val());
  
        const data = {
          password: password
        };
  
        if (grecaptcha.getResponse()) { // Check if reCAPTCHA is completed
          await fetch("/registerRequest", {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
              "Accept": "application/json"
            },
            body: JSON.stringify(data),
          })
          .then(response => 
          {
            // redirect to login if registration successful
            if (response.ok) {
              window.location.href = "/login";
            }
          });
        } else {
          document.getElementById("error-message").textContent = "Please complete the reCAPTCHA.";
        }
      }
    });
  });
  
  (function($) {
    $('.palceholder').click(function() {
      $(this).siblings('input').focus();
    });
  
    $('.form-control').focus(function() {
      $(this).parent().addClass("focused");
    });
  
    $('.form-control').blur(function() {
      var $this = $(this);
      if ($this.val().length == 0)
        $(this).parent().removeClass("focused");
    });
    $('.form-control').blur();  
  
    $.validator.setDefaults({
      errorElement: 'span',
      errorClass: 'validate-tooltip'
    });
  
    $("#register-form").validate({
      rules: {
        userPassword: {
          required: true,
          minlength: 12,
          maxlength: 32,
          customPasswordValidation: true,
        }
      },
      messages: {
        userPassword: {
          required: "Please enter your password.",
          minlength: "Password must be at least 12 characters long.",
          maxlength: "Password cannot be more than 32 characters long.",
          customPasswordValidation: "Please provide a valid password."
        }
      }
    });
    
    $.validator.addMethod("customPasswordValidation", function(value, element) {
      var passwordPattern = /^.{12,32}$/;
      return passwordPattern.test(value);
    }, "Please provide a valid password.");
  })(jQuery);
  