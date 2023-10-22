document.addEventListener("DOMContentLoaded", function () {
    $("#login-button").click(async function (event) {
      event.preventDefault();
  
      if ($("#formvalidate").valid()) {
        const username = $("#userName").val();
        const password = $("#userPassword").val();
  
        const data = {
          username: username,
          password: password
        };
  
        await fetch("/loginRequest", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            "Accept": "application/json"
          },
          body: JSON.stringify(data),
        })
        .then(response => response.json())
        .then(data => {
          console.log(document.cookie);
          // TODO: REPLACE WITH LOGIN SUCCESS CODE
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
  