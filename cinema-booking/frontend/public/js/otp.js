// iterate over all inputs
$('#otp').each((index1, input) => {
    $(input).on("keyup", (e) => {
        // gets the current input element and stores it in the currentInput variable
        // gets the next sibling element of the current input element and stores it in the nextInput variable
        // gets the previous sibling element of the current input element and stores it in the prevInput variable
        const currentInput = $(input),
            nextInput = $(input).next(),
            prevInput = $(input).prev();
        
        // Allow only alphanumeric characters
        const sanitizedValue = currentInput.val().replace(/[^a-zA-Z0-9]/g, '');
        if (currentInput.val() !== sanitizedValue) {
        currentInput.val(sanitizedValue);
        return; // Exit if non-alphanumeric characters were removed
        }

        // if the value has more than one character then clear it
        if (sanitizedValue.length > 1) {
        currentInput.val("");
        return;
        }
        
        // if the next input is disabled and the current value is not empty
        // enable the next input and focus on it
        if (nextInput && nextInput.is(':disabled') && sanitizedValue !== "") {
            nextInput.removeAttr("disabled");
            nextInput.focus();
        }

        // if the backspace key is pressed
        if (e.key === "Backspace") {
            // iterate over all inputs again
            $('input').each((index2, input2) => {
            // if the index1 of the current input is less than or equal to the index2 of the input in the outer loop
            // and the previous element exists, set the disabled attribute on the input and focus on the previous element
            if (index1 <= index2 && prevInput) {
                $(input2).prop("disabled", true);
                $(input2).val("");
                prevInput.focus();
            }
            });
        }

        // if the 6th input( which index number is 5) is not empty and has not disable attribute then
        // add active class if not then remove the active class.
        if (!$('input').eq(5).prop('disabled') && $('input').eq(5).val() !== "") {
            button.addClass("active");
            return;
        }
        button.removeClass("active");
    });
});

const otpForm = $('#otp-form'); // replace 'otpForm' with the actual id of your form

otpForm.on('submit', async function (e) {
    e.preventDefault(); // prevent the default form submission

    // get the form data
    const otpValues = $('.otp-input').map(function() {
        return $(this).val();
    }).get();

    await fetch("/otpRequest", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "Accept": "application/json"
        },
        body: JSON.stringify(otpValues),
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