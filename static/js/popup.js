 // Function to hide flashed messages after a certain time
 document.addEventListener('DOMContentLoaded', function () {
    setTimeout(function() {
        document.querySelectorAll('.alert').forEach(function(alert) {
            alert.style.display = 'none';
        });
    }, 3000); // Adjust the time as needed (3 seconds in this example)
});

        
        
