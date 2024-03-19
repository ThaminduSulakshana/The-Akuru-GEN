// script.js
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
