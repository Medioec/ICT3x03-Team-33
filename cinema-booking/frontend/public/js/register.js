// Define a function to check if all registration fields and the form are valid
function checkRegistrationFields() {
  const $emailInput = $("#email");
  const $userNameInput = $("#userName");
  const $userPasswordInput = $("#userPassword");
  const isFormValid = $("#register-form").valid(); // Check overall form validity

  // Return true if all fields are filled correctly and the form is valid
  return $emailInput.val() && $userNameInput.val() && $userPasswordInput.val() && isFormValid;
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
  const $emailInput = $("#email");
  const $userNameInput = $("#userName");
  const $userPasswordInput = $("#userPassword");

  $emailInput.on("input", function () {
    if (checkRegistrationFields()) {
      onSuccess(); 
    } else {
      $("#register-button").prop("disabled", true);
    }
  });

  $userNameInput.on("input", function () {
    if (checkRegistrationFields()) {
      onSuccess(); 
    } else {
      $("#register-button").prop("disabled", true);
    }
  });

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
      const email = $emailInput.val();
      const username = $userNameInput.val();
      const password = $userPasswordInput.val();

      const data = {
        email: email,
        username: username,
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
        .then(response => response.json())
        .then(data => {
          // TODO: REPLACE WITH LOGIN SUCCESS CODE
          document.getElementById("error-message").textContent = data.message;
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
      email: {
        required: true,
        customEmailValidation: true,
      },
      username: {
        required: true,
        minlength: 3,
        customUsernameValidation: true
      },
      userPassword: {
        required: true,
        minlength: 12,
        maxlength: 32,
        customPasswordValidation: true,
      }
    },
    messages: {
      email: {
        required: "Please enter your email address.",
        customEmailValidation: "Please provide a valid email address."
      },
      username: {
        required: "Please enter your username.",
        minlength: "Username must be at least 3 characters.",
        customUsernameValidation: "Please provide a valid username."
      },
      userPassword: {
        required: "Please enter your password.",
        minlength: "Password must be at least 12 characters long.",
        maxlength: "Password cannot be more than 32 characters long.",
        customPasswordValidation: "Please provide a valid password."
      }
    }
  });

  $.validator.addMethod("customEmailValidation", function(value, element) {
    var emailPattern = /^[A-Za-z0-9_!#$%&'*+\/=?^_`{|}~.-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$/;
    return emailPattern.test(value);
  }, "Please provide a valid email address.");

  $.validator.addMethod("customUsernameValidation", function(value, element) {
    var usernamePattern = /^[a-zA-Z0-9]{3,16}$/;
    return usernamePattern.test(value);
  }, "Please provide a valid username.");
  
  $.validator.addMethod("customPasswordValidation", function(value, element) {
    var passwordPattern = /^.{12,32}$/;
    return passwordPattern.test(value);
  }, "Please provide a valid password.");
})(jQuery);
