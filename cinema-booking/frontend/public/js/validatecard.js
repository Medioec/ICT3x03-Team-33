// Define the onSuccess function to handle the captcha callback
function onSuccess() {
  if (grecaptcha.getResponse()) {
    captchaState = true;
    console.log(captchaState);
    captchaFeedback.textContent = "";
  }
}

let captchaState = false;
const captchaFeedback = document.getElementById("captchaError");

document.addEventListener('DOMContentLoaded', function() {

  (() => {
    "use strict";

    const form = document.querySelector(".needs-validation");
    const creditCardNumberInput = document.getElementById("creditCardNumber");
    const creditCardNameInput = document.getElementById("creditCardName");
    const creditCardExpiryInput = document.getElementById("creditCardExpiry");
    const cvvInput = document.getElementById("cvv");

    //////////////////////////////////////////////////////////////////////////

    const creditCardNumberFeedback = document.createElement("div");
    creditCardNumberFeedback.className = "invalid-feedback";
    creditCardNumberFeedback.textContent = "Invalid card number";
    creditCardNumberInput.parentNode.appendChild(creditCardNumberFeedback);

    const creditCardNameFeedback = document.createElement("div");
    creditCardNameFeedback.className = "invalid-feedback";
    creditCardNameFeedback.textContent = "Invalid card name";
    creditCardNameInput.parentNode.appendChild(creditCardNameFeedback);

    const creditCardExpiryFeedback = document.createElement("div");
    creditCardExpiryFeedback.className = "invalid-feedback";
    creditCardExpiryFeedback.textContent = "Invalid expiry date";
    creditCardExpiryInput.parentNode.appendChild(creditCardExpiryFeedback);

    const cvvFeedback = document.createElement("div");
    cvvFeedback.className = "invalid-feedback";
    cvvFeedback.textContent = "Invalid CVV";
    cvvInput.parentNode.appendChild(cvvFeedback);

    form.addEventListener(
      "submit",
      (event) => {
        // Sanitize the input using DOMPurify before validation
        const sanitizedCreditCardNumber = DOMPurify.sanitize(
          creditCardNumberInput.value
        );
        const sanitizedCreditCardName = DOMPurify.sanitize(
          creditCardNameInput.value
        );
        const sanitizedCreditCardExpiry = DOMPurify.sanitize(
          creditCardExpiryInput.value
        );
        const sanitizedCvv = DOMPurify.sanitize(cvvInput.value);

        console.log("1", cvvInput.value);

        console.log("2", sanitizedCvv);

        const formData = {
          creditCardNumber: sanitizedCreditCardNumber,
          creditCardName: sanitizedCreditCardName,
          creditCardExpiry: sanitizedCreditCardExpiry,
          cvv: sanitizedCvv,
        };

        console.log("3", formData);

        const creditCardData = JSON.stringify(formData);
        if (!form.checkValidity() || captchaState === false) {
          event.preventDefault();
          event.stopPropagation();
          captchaFeedback.textContent = "Please complete the captcha!";
        } else {
          fetch("/addcreditcard", {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
              Accept: "application/json",
            },
            body: creditCardData,
          })
            .then((response) => {
              if (response.ok) {
                alert("Credit card added successfully");
                window.location.reload();
              }
            })

            .catch((error) => {
              console.error("Error occurred", error);
            });
        }

        form.classList.add("was-validated");
      },
      false
    );

    function validateCreditCardNumber(creditCardNumber) {
      // regex to check if the cc number contains only numbers
      if (!/^\d+$/.test(creditCardNumber)) {
        return false;
      }
      // Check if the card number has a valid length
      if (creditCardNumber.length < 13 || creditCardNumber.length > 19) {
        return false;
      }
      return true;
    }

    function validateCreditCardName(creditCardName) {
      return /^[A-Za-z\s]+$/.test(creditCardName) && creditCardName.length > 0;
    }

    function validateCreditCardExpiry(creditCardExpiry) {
      try {
        if (
          creditCardExpiry.length !== 5 ||
          !/^(0[1-9]|1[0-2])\/\d{2}$/.test(creditCardExpiry)
        ) {
          return false;
        }

        const month = parseInt(creditCardExpiry.substring(0, 2), 10) - 1;
        const year = parseInt(`20${creditCardExpiry.substring(3, 5)}`, 10);

        const expiryDate = new Date(year, month, 1);
        const currentDate = new Date();

        return expiryDate > currentDate;
      } catch (error) {
        return false;
      }
    }

    function validateCvv(cvv) {
      return /^\d{3,4}$/.test(cvv);
    }

    //////////////////////////////////////////////////////////////////////////

    // Delete Credit Card Modal
    const deleteButtons = document.querySelectorAll(
      '.btn-danger[data-toggle="modal"]'
    );
    const deleteCardModal = document.getElementById("deleteCardModal");
    const confirmDeleteCardButton = document.getElementById("confirmDeleteCard");
    const deleteMessage = document.getElementById("deleteBody");

    // dismiss modals
    const dismissButtonsDel = document.querySelectorAll('.closeModal');

    dismissButtonsDel.forEach((button) => {
      button.addEventListener('click', function () {
        console.log("dismissed");
        deleteCardModal.style.display = "none";
      });
    });

    deleteButtons.forEach((button) => {
      button.addEventListener("click", async (event) => {
        // Show the deleteCardModal
        deleteCardModal.style.display = "block";
    
        // Retrieve the credit card number from the clicked button
        const creditCardNumber = button.getAttribute("data-card-number");
    
        // Find the corresponding creditCardId based on the creditCardNumber from creditCardData
        const matchingCard = creditCardData.find((card) => card.creditCardNumber === creditCardNumber);
        
        console.log("inside matched", matchingCard);

        if (!matchingCard) {
          // Handle the case where a matching card is not found in creditCardData
          console.error("Matching card not found in creditCardData");
          return;
        }
    
        // Display a confirmation message in the modal
        const deleteMessage = document.getElementById("deleteBody");
        deleteMessage.textContent = `Are you sure you want to delete the credit card with number ${creditCardNumber}?`;
    
        // Create a creditCard object with the found creditCardId
        const creditCardId = matchingCard.creditCardId;
    
        console.log("after matched", creditCardId);

        const creditCardNo = JSON.stringify(creditCardId);

        console.log("after JSON", creditCardNo);

        const creditCardFinal = JSON.stringify({ creditCardId });

        console.log("after final", creditCardFinal);

        // Add a confirm delete action
        confirmDeleteCardButton.addEventListener("click", async () => {
          fetch("/deletecreditcard", {
            method: "DELETE",
            headers: {
              "Content-Type": "application/json",
              Accept: "application/json",
            },
            body: creditCardFinal,
          })
            .then((response) => {
              if (response.ok) {
                alert("Credit card deleted successfully");
                window.location.reload();
              }
            })
            .catch((error) => {
              console.error("Error occurred", error);
            });
        });
      });
    });

    // Modify Credit Card Modal
    const modifyButtons = document.querySelectorAll('.btn-primary[data-toggle="modal"]');
    const modifyCardModal = document.getElementById("modifyCardModal");

    // dismiss modals
    const dismissButtonsMod = document.querySelectorAll('.closeModalMod');

    dismissButtonsMod.forEach((button) => {
      button.addEventListener('click', function () {
        console.log("dismissed");
        modifyCardModal.style.display = "none";
      });
    });

    modifyButtons.forEach((button) => {
      button.addEventListener("click", async (event) => {
        modifyCardModal.style.display = "block";
    
        // Retrieve the credit card information from the clicked button
        const cardNumber = button.getAttribute("data-card-no");
        const cardName = button.getAttribute("data-card-name");
        const cardExpiry = button.getAttribute("data-card-expiry");
        const cardCVV = button.getAttribute("data-card-cvv");

        console.log("card number", cardNumber);
        console.log("card name", cardName);
        console.log("card expiry", cardExpiry);
        console.log("card cvv", cardCVV);
    
        // Select the input fields within the modal's body using the data-field-id attribute
        const cardNumberInput = document.querySelector('input[data-field-id="cardNumber"]');
        const cardNameInput = document.querySelector('input[data-field-id="cardName"]');
        const cardExpiryInput = document.querySelector('input[data-field-id="cardExpiry"]');
        const cardCVVInput = document.querySelector('input[data-field-id="cardCVV"]');

        console.log("card number input", cardNumberInput);
        console.log("card name input", cardNameInput);
        console.log("card expiry input", cardExpiryInput);
        console.log("card cvv input", cardCVVInput);
    
        // Update the values of the input fields with the retrieved information
        cardNumberInput.value = cardNumber;
        cardNameInput.value = cardName;
        cardExpiryInput.value = cardExpiry;
        cardCVVInput.value = cardCVV;
      });
    });

    //////////////////////////////////////////////////////////////////////////

    creditCardNumberInput.addEventListener("input", () => {
      if (!validateCreditCardNumber(creditCardNumberInput.value)) {
        creditCardNumberInput.setCustomValidity("Invalid card number");
        creditCardNumberFeedback.style.display = "block";
      } else {
        creditCardNumberInput.setCustomValidity("");
        creditCardNumberFeedback.style.display = "none";
      }
    });

    creditCardNameInput.addEventListener("input", () => {
      if (!validateCreditCardName(creditCardNameInput.value)) {
        creditCardNameInput.setCustomValidity("Invalid card name");
        creditCardNameFeedback.style.display = "block";
      } else {
        creditCardNameInput.setCustomValidity("");
        creditCardNameFeedback.style.display = "none";
      }
    });

    creditCardExpiryInput.addEventListener("input", () => {
      if (!validateCreditCardExpiry(creditCardExpiryInput.value)) {
        creditCardExpiryInput.setCustomValidity("Invalid expiry date");
        creditCardExpiryFeedback.style.display = "block";
      } else {
        creditCardExpiryInput.setCustomValidity("");
        creditCardExpiryFeedback.style.display = "none";
      }
    });

    cvvInput.addEventListener("input", () => {
      const cvvValue = cvvInput.value;
      const isValidCvv = validateCvv(cvvValue);
    
      if (!isValidCvv) {
        cvvInput.setCustomValidity("Invalid CVV");
        cvvFeedback.style.display = "block";
      } else {
        cvvInput.setCustomValidity("");
        cvvFeedback.style.display = "none";
      }
    });
    

    //////////////////////////////////////////////////////////////////////////
  })();
});
