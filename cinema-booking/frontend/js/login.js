(function($) {
  function isUsernameValid(username) {
    var pattern = /^[a-zA-Z0-9]{3,16}$/;
    return pattern.test(username);
  }

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
    return isUsernameValid(value);
  }, "Please provide a valid username.");

})(jQuery);
