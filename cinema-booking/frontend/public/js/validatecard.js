(() => {
    'use strict';
  
    const form = document.querySelector('.needs-validation');
    const creditCardNumberInput = document.getElementById('creditCardNumber');
    const creditCardNameInput = document.getElementById('creditCardName');
    const creditCardExpiryInput = document.getElementById('creditCardExpiry');
    const cvvInput = document.getElementById('cvv');

    //////////////////////////////////////////////////////////////////////////

    const creditCardNumberFeedback = document.createElement('div');
    creditCardNumberFeedback.className = 'invalid-feedback';
    creditCardNumberFeedback.textContent = 'Invalid card number';
    creditCardNumberInput.parentNode.appendChild(creditCardNumberFeedback);
  
    const creditCardNameFeedback = document.createElement('div');
    creditCardNameFeedback.className = 'invalid-feedback';
    creditCardNameFeedback.textContent = 'Invalid card name';
    creditCardNameInput.parentNode.appendChild(creditCardNameFeedback);
  
    const creditCardExpiryFeedback = document.createElement('div');
    creditCardExpiryFeedback.className = 'invalid-feedback';
    creditCardExpiryFeedback.textContent = 'Invalid expiry date';
    creditCardExpiryInput.parentNode.appendChild(creditCardExpiryFeedback);
  
    const cvvFeedback = document.createElement('div');
    cvvFeedback.className = 'invalid-feedback';
    cvvFeedback.textContent = 'Invalid CVV';
    cvvInput.parentNode.appendChild(cvvFeedback);
  
    //////////////////////////////////////////////////////////////////////////

    form.addEventListener('submit', (event) => {
        // Sanitize the input using DOMPurify before validation
        const sanitizedCreditCardNumber = DOMPurify.sanitize(creditCardNumberInput.value);
        const sanitizedCreditCardName = DOMPurify.sanitize(creditCardNameInput.value);
        const sanitizedCreditCardExpiry = DOMPurify.sanitize(creditCardExpiryInput.value);
        const sanitizedCvv = DOMPurify.sanitize(cvvInput.value);
        
        if (!form.checkValidity()) {
            event.preventDefault();
            event.stopPropagation();
        }

      form.classList.add('was-validated');
    }, false);
  
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
          if (creditCardExpiry.length !== 5 || creditCardExpiry.charAt(2) !== '/') {
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

    //////////////////////////////////////////////////////////////////////////

    creditCardNumberInput.addEventListener('input', () => {
      if (!validateCreditCardNumber(creditCardNumberInput.value)) {
        creditCardNumberInput.setCustomValidity('Invalid card number');
        creditCardNumberFeedback.style.display = 'block';
      } else {
        creditCardNumberInput.setCustomValidity('');
        creditCardNumberFeedback.style.display = 'none';
      }
    });
  
    creditCardNameInput.addEventListener('input', () => {
      if (!validateCreditCardName(creditCardNameInput.value)) {
        creditCardNameInput.setCustomValidity('Invalid card name');
        creditCardNameFeedback.style.display = 'block';
      } else {
        creditCardNameInput.setCustomValidity('');
        creditCardNameFeedback.style.display = 'none';
      }
    });
  
    creditCardExpiryInput.addEventListener('input', () => {
      if (!validateCreditCardExpiry(creditCardExpiryInput.value)) {
        creditCardExpiryInput.setCustomValidity('Invalid expiry date');
        creditCardExpiryFeedback.style.display = 'block';
      } else {
        creditCardExpiryInput.setCustomValidity('');
        creditCardExpiryFeedback.style.display = 'none';
      }
    });
  
    cvvInput.addEventListener('input', () => {
      if (!validateCvv(cvvInput.value)) {
        cvvInput.setCustomValidity('Invalid CVV');
        cvvFeedback.style.display = 'block';
      } else {
        cvvInput.setCustomValidity('');
        cvvFeedback.style.display = 'none';
      }
    });
    
    //////////////////////////////////////////////////////////////////////////

  })();
  