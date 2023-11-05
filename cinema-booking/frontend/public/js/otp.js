// iterate over all inputs
$('.otp-input').each((index1, input) => {
    $(input).on("keyup", (e) => {
        // gets the current input element and stores it in the currentInput variable
        // gets the next sibling element of the current input element and stores it in the nextInput variable
        const currentInput = $(input),
            nextInput = currentInput.next();

        // Get the current value and convert it to uppercase
        let sanitizedValue = currentInput.val().toUpperCase();

        // Allow only a single alphanumeric character
        sanitizedValue = sanitizedValue.replace(/[^A-Z0-9]/g, '').substr(0, 1);

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

            // Clear all inputs and OTP values
            $('.otp-input').val('');

            // Disable all fields except for the first field
            $('.otp-input:not(:first)').prop('disabled', true);

            // Remove the 'required' attribute from all fields except for the first field
            $('.otp-input:not(:first)').removeAttr('required');
            
            // Focus on the first input
            $('input').eq(0).focus();

            throw new Error(data.message);
        }

        // if token expired, redirect to login page
        else if (data.status === 'expired') {
            document.getElementById("error-message").textContent = data.message;
            setTimeout(() => window.location.href = "/login", 1500);
        }


        switch (data.userRole) {
            case "member":
              window.location.href = "/member";
              break;
      
            case "staff":
              window.location.href = "/staff";
              break;

            case "admin":
                window.location.href = "/createStaff";
                break;
        }
    })
});


// focus the first input which index is 0 on window load
$(window).on("load", () => $('input').eq(0).focus());  