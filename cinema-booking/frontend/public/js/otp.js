// iterate over all inputs
$('.otp-input').each((index1, input) => {
    $(input).on("keyup", (e) => {
        // gets the current input element and stores it in the currentInput variable
        // gets the next sibling element of the current input element and stores it in the nextInput variable
        const currentInput = $(input),
            nextInput = currentInput.next();

        // Get the current value and convert it to uppercase
        let sanitizedValue = currentInput.val().toUpperCase();

        // Allow only alphanumeric characters
        sanitizedValue = sanitizedValue.replace(/[^A-Z0-9]/g, '');

        // Update the input field with the uppercase sanitized value
        currentInput.val(sanitizedValue);

        // if the next input exists and the current value is not empty
        // focus on the next input
        if (nextInput.length > 0 && sanitizedValue !== "") {
            nextInput.removeAttr('disabled').attr('required', 'required').focus(); // remove the disabled attribute and add the required attribute
        }
    });
});


const otpForm = $('#otp-form'); // replace 'otpForm' with the actual id of your form

otpForm.on('submit', function (e) {
    e.preventDefault(); // prevent the default form submission

    // get the form data and join the OTP values into a single string
    const otpValues = $('.otp-input').map(function() {
        return $(this).val();
    }).get().join('');

    console.log("otpvalues", otpValues);
    
    fetch("/otpRequest", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "Accept": "application/json"
        },
        body: JSON.stringify({"otp": otpValues}),
    })
    .then(response => {
        return response.json(); // Parse response as JSON
    })
    .then(data => {
        if (data.status === 'fail') {
          document.getElementById("error-message").textContent = data.message;
          throw new Error(data.message);
        }

        switch (data.userRole) {
            case "member":
              window.location.href = "/member";
              break;
      
            case "staff":
              window.location.href = "/staff";
              break;

            // TODO ADD A CASE FOR ADMIN
        }
    })
});


// focus the first input which index is 0 on window load
$(window).on("load", () => $('input').eq(0).focus());  