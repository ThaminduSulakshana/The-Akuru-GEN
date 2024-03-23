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
        description.innerHTML = 'This is the Free subscription level. Lorem ipsum dolor sit amet, consectetur adipiscing elit.';
    } else if (level === 'standard') {
        title.innerHTML = 'Standard Package';
        description.innerHTML = 'This is the Standard subscription level. Lorem ipsum dolor sit amet, consectetur adipiscing elit.';
    } else if (level === 'premium') {
        title.innerHTML = 'Premium Package';
        description.innerHTML = 'This is the Premium subscription level. Lorem ipsum dolor sit amet, consectetur adipiscing elit.';
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