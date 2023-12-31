// Define a function to check if username and password are filled correctly
function checkUsernamePassword() {
  const $userNameInput = $("#userName");
  const $userPasswordInput = $("#userPassword");
  return $userNameInput.val() && $userPasswordInput.val();
}

// Define the onSuccess function to handle the captcha callback
function onSuccess() {
  const $loginButton = $("#login-button");
  if (checkUsernamePassword() && grecaptcha.getResponse()) {
    $loginButton.prop("disabled", false);
  }
}

document.addEventListener("DOMContentLoaded", function () {
  const $loginButton = $("#login-button");
  const $userNameInput = $("#userName");
  const $userPasswordInput = $("#userPassword");

  $userNameInput.on("input", function () {
    if (checkUsernamePassword()) {
      onSuccess(); // Check and enable the login button
    }
  });

  $userPasswordInput.on("input", function () {
    if (checkUsernamePassword()) {
      onSuccess(); // Check and enable the login button
    }
  });

  $loginButton.click(async function (event) {
    event.preventDefault();

    if ($("#login-form").valid()) {
      // Sanitize the username and password inputs using DOMPurify
      const username = DOMPurify.sanitize($userNameInput.val());
      const password = DOMPurify.sanitize($userPasswordInput.val());

      const data = {
        username: username,
        password: password
      };

      if (grecaptcha.getResponse()) { // Check if reCAPTCHA is completed
        await fetch("/loginRequest", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            "Accept": "application/json"
          },
          body: JSON.stringify(data),
        })
        .then(response => {
          return response.json(); // Parse response as JSON
        })
        .then(data => {
          if (data.status === 'fail') {
            document.getElementById("error-message").textContent = data.message;
            throw new Error(data.message);
          }

          else if (data.status === 'success') {
            window.location.href = "/otp";
          }
        })
        .catch(error => {
          console.error("Error:", error.message);
          // Handle the error as needed
        });
      
      } else {
        document.getElementById("error-message").textContent ="Please complete the reCAPTCHA.";
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

  $("#login-form").validate({
    rules: {
      userName: {
        required: true,
        minlength: 3,
        customUsernameValidation: true
      },
      userPassword: {
        required: true
      }
    },
    messages: {
      userName: {
        required: "Please enter your username.",
        minlength: "Username must be at least 3 characters.",
        customUsernameValidation: "Please provide a valid username."
      },
      userPassword: {
        required: "Please enter your password."
      }
    }
  });

  $.validator.addMethod("customUsernameValidation", function(value, element) {
    var pattern = /^[a-zA-Z0-9]{3,16}$/;
    return pattern.test(value);
  }, "Please provide a valid username.");
  
  })(jQuery);
  