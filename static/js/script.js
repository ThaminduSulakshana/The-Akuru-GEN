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

//selectSubscription function takes one parameter level
function selectSubscription(level) {
    const subscriptionBoxes = document.querySelectorAll('.box');
    const hiddenInput = document.getElementById('selected_subscription_level');
    
    // Remove 'selected' class from all subscription boxes
    subscriptionBoxes.forEach(box => {
    });
    
    // Update the hidden input field value with the selected level
    hiddenInput.value = level;
    
    // Submit the form when a subscription box is clicked
    document.getElementById('subscriptionForm').submit();
}