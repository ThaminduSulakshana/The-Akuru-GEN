// Function to validate card number
function validateCardNumber(cardNumber) {
    return /^\d{16}$/.test(cardNumber);
}

// Function to detect card type
function detectCardType(cardNumber) {
    if (/^4/.test(cardNumber)) {
        return 'visa';
    } else if (/^5[1-5]/.test(cardNumber)) {
        return 'mastercard';
    } else {
        return 'unknown';
    }
}

// Function to validate expiry date
function validateExpiryDate(expiryDate) {
    return /^(0[1-9]|1[0-2])\/\d{2}$/.test(expiryDate);
}

// Function to validate CVV
function validateCVV(cvv) {
    return /^\d{3}$/.test(cvv);
}

document.addEventListener('DOMContentLoaded', function() {
    // Select input fields
    const cardNumberInput = document.getElementById('card_number');
    const expiryDateInput = document.getElementById('expiry_date');
    const cvvInput = document.getElementById('cvv');

    // Select feedback spans
    const cardNumberFeedback = document.getElementById('card-number-feedback');
    const expiryDateFeedback = document.getElementById('expiry-date-feedback');
    const cvvFeedback = document.getElementById('cvv-feedback');

    // Function to update feedback
    function updateFeedback(input, feedback, isValid, hint) {
        if (isValid) {
            input.classList.remove('is-invalid');
            input.classList.add('is-valid');
            feedback.innerHTML = '';
        } else {
            input.classList.remove('is-valid');
            input.classList.add('is-invalid');
            feedback.innerHTML = `<div class="invalid-feedback">Invalid input. ${hint}</div>`;
        }
    }

    // Event listeners for input fields
    cardNumberInput.addEventListener('input', function() {
        const isValid = validateCardNumber(this.value);
        const cardType = detectCardType(this.value);
        const hint = 'Please enter a 16-digit card number.';
        updateFeedback(this, cardNumberFeedback, isValid, hint);
        // Display card icon based on card type
        const cardIcon = document.getElementById('card-icon');
        if (cardType === 'visa') {
            cardIcon.className = 'fab fa-cc-visa text-success';
        } else if (cardType === 'mastercard') {
            cardIcon.className = 'fab fa-cc-mastercard text-success';
        } else {
            cardIcon.className = '';
        }
    });

    expiryDateInput.addEventListener('input', function() {
        // Add slash automatically after 2 characters
        if (this.value.length === 2 && !this.value.includes('/')) {
            this.value += '/';
        }
        const isValid = validateExpiryDate(this.value);
        const hint = 'Please enter a valid expiry date in MM/YYYY format.';
        updateFeedback(this, expiryDateFeedback, isValid, hint);
    });

    cvvInput.addEventListener('input', function() {
        const isValid = validateCVV(this.value);
        const hint = 'Please enter a 3-digit CVV.';
        updateFeedback(this, cvvFeedback, isValid, hint);
    });
});
