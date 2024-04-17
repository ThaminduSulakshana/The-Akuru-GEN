// Function to redirect to the pages
function redirectToRegister() {
    window.location.href = "/register"; // Adjust the URL as needed
}

function redirectToQanswering() {
    window.location.href = "/Qanswering"; // Adjust the URL as needed
}

function redirectTotranslate() {
    window.location.href = "/translate"; // Adjust the URL as needed
}

function redirectsub() {
    window.location.href = "/subscribe"; // Adjust the URL as needed
}

// Function to detect language using AJAX request to Flask server
function detectLanguage() {
    var inputText = document.getElementById('input_text').value;
    var detectedLanguageElement = document.getElementById('detected_language');

    // Make an AJAX request to the Flask server for language detection
    var xhr = new XMLHttpRequest();
    xhr.open('POST', '/detect_language', true);
    xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
    xhr.onreadystatechange = function() {
        if (xhr.readyState == 4 && xhr.status == 200) {
            var detectedLanguage = xhr.responseText;
            detectedLanguageElement.innerHTML = 'Detected Language: ' + detectedLanguage;
        }
    };
    xhr.send('input_text=' + encodeURIComponent(inputText));

    // Allow the form to be submitted
    return true;
}
gg
// Function to show subscription information based on selected level
function showSubscriptionInfo(level) {
    var title = document.getElementById('subscriptionTitle'); // Get the title element
    var description = document.getElementById('subscriptionDescription'); // Get the description element
    var infoBox = document.getElementById('subscriptionInfo'); // Get the subscription info box element
    var selectedSubscription = document.getElementById('selected_subscription_level'); // Get the selected subscription level input
    var selectButton = document.getElementById('selectButton'); // Get the select button element
    var billingForm = document.getElementById('billingForm'); // Get the billing form

    // Update title and description based on selected level
    if (level === 'free') {
        title.innerHTML = 'Free Package';
        description.innerHTML = 'Upgrade to the Basic Plan for $39.99/month with a 1-week free trial!';
    } else if (level === 'standard') {
        title.innerHTML = 'Standard Package';
        description.innerHTML = 'Upgrade to the Standard Plan for $59.99/month with a 1-week free trial!';
    } else if (level === 'premium') {
        title.innerHTML = 'Premium Package';
        description.innerHTML = 'Upgrade to the Premium Plan for $99.99/month with a 1-week free trial!';
    }

    selectedSubscription.value = level; // Set the selected subscription level
    infoBox.classList.remove('hidden'); // Remove the 'hidden' class to show the subscription info box
    selectButton.style.display = 'block'; // Show the select button

    // Show the billing form when a subscription is selected
    billingForm.style.display = 'block';
}

// JavaScript function to submit the selected subscription level
function selectSubscription() {
    document.getElementById('subscriptionForm').submit(); // Submit the subscription form
}


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


 // Selecting form, email field, and password field
 