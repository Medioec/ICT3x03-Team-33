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

    //////////////////////////////////////////////////////////////////////////

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

        const formData = {
          creditCardNumber: sanitizedCreditCardNumber,
          creditCardName: sanitizedCreditCardName,
          creditCardExpiry: sanitizedCreditCardExpiry,
          cvv: sanitizedCvv,
        };

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

    //////////////////////////////////////////////////////////////////////////

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
        const creditCardId = button.getAttribute("data-card-id");
        console.log("credit card number", creditCardNumber)
    
        // Display a confirmation message in the modal
        const deleteMessage = document.getElementById("deleteBody");
        deleteMessage.textContent = `Are you sure you want to delete the credit card with number ${creditCardId}?`;
    
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
        modifyCardModal.style.display = "none";
      });
    });

    modifyButtons.forEach((button) => {
      button.addEventListener("click", async (event) => {
        const cardId = button.getAttribute("data-card-id");
        const cardNumber = button.getAttribute("data-card-number");
        const cardExpiry = button.getAttribute("data-card-expiry");
        const cardName = button.getAttribute("data-card-name");
        const cardCVV = button.getAttribute("data-card-cvv");
    
        document.getElementById("cardId").value = cardId;
        document.getElementById("cardNumber").value = cardNumber;
        document.getElementById("cardName").value = cardName;
        document.getElementById("cardExpiry").value = cardExpiry;
        document.getElementById("modalCVV").value = cardCVV;
    
        modifyCardModal.style.display = "block";
    
        document.getElementById("confirmModifyCard").addEventListener("click", async (e) => {
          e.preventDefault();
    
          const modifiedCardData = {
            creditCardId: cardId,
            creditCardNumber: document.getElementById("cardNumber").value,
            creditCardName: document.getElementById("cardName").value,
            creditCardExpiry: document.getElementById("cardExpiry").value,
            cvv: document.getElementById("modalCVV").value,
          };
    
          try {
            const response = await fetch("/modifycreditcard", {
              method: "PUT",
              headers: {
                "Content-Type": "application/json",
                Accept: "application/json",
              },
              body: JSON.stringify(modifiedCardData), // Ensure data is sent as JSON
            });
    
            if (response.ok) {
              alert("Credit card modified successfully");
              modifyCardModal.style.display = "none"; // Close the modal
              window.location.reload(); // Reload the page
            } else {
              // Handle the case where the request was not successful (e.g., display an error message)
              console.error("Error occurred. Status: " + response.status);
            }
          } catch (error) {
            // Handle network or fetch-related errors
            console.error("Error occurred", error);
          }
        });
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


  ///////////////////////////////////////////////////////////////////////////////////////////////////////////

  