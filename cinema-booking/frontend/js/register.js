document.addEventListener("DOMContentLoaded", function () {
    $("#register-button").click(async function (event) {
      event.preventDefault();
  
      if ($("#formvalidate").valid()) {
        const email = $("#email").val();
        const username = $("#username").val();
        const password = $("#userPassword").val();
  
        // Validate using custom functions
        if (!isEmailValid(email)) {
          handleValidationFailure("Please provide a valid email address.");
          return;
        }
        if (!isUsernameValid(username)) {
          handleValidationFailure("Please provide a valid username.");
          return;
        }
        if (!isPasswordValid(password)) {
          handleValidationFailure("Please use a valid password format.");
          return;
        }
  
        // If all validations pass, proceed with the fetch request
        const data = {
          email: email,
          username: username,
          password: password
        };
  
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
          console.log(data.message);
          document.getElementById("error-message").textContent = data.message;
        });
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
  
    $("#formvalidate").validate({
      rules: {
        email: {
          required: true,
          email: true,
        },
        username: {
          required: true,
          minlength: 3,
          maxlength: 16,
        },
        userPassword: {
          required: true,
          minlength: 8,
          maxlength: 32,
        },
      },
      messages: {
        email: {
          required: "Please enter your email address.",
        },
        username: {
          required: "Please enter your username.",
          minlength: "Username must be at least 3 characters long.",
          maxlength: "Username cannot be more than 16 characters long.",
        },
        userPassword: {
          required: "Please enter your password.",
          minlength: "Password must be at least 8 characters long.",
          maxlength: "Password cannot be more than 32 characters long.",
        },
      }
    });
  })(jQuery);
  
  function isEmailValid(email) {
    var emailPattern = /^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$/;
    return emailPattern.test(email);
  }
  
  function isUsernameValid(username) {
    var usernamePattern = /^[a-zA-Z0-9]{3,16}$/;
    return usernamePattern.test(username);
  }
  
  function isPasswordValid(password) {
    var passwordPattern = /^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[^A-Za-z\d]).{8,32}$/;
    return passwordPattern.test(password);
  }
  
  function handleValidationFailure(errorMessage) {
    document.getElementById("error-message").textContent = errorMessage;
  }
  