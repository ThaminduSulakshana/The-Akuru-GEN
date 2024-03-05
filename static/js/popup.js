function displayErrorPopup(errorMessage) {
    var errorTooltip = document.createElement("div");
    errorTooltip.innerHTML = errorMessage;
    errorTooltip.style.position = "fixed";
    errorTooltip.style.top = "10%";
    errorTooltip.style.left = "50%";
    errorTooltip.style.transform = "translateX(-50%)";
    errorTooltip.style.padding = "10px";
    errorTooltip.style.backgroundColor = "#1583f0a6";
    errorTooltip.style.color = "#fff";
    errorTooltip.style.borderRadius = "5px";
    errorTooltip.style.zIndex = "1000";
    errorTooltip.style.boxShadow = "0 0 10px rgba(0, 0, 0, 0.3)";
    document.body.appendChild(errorTooltip);

    // Hide the errorTooltip after 3 seconds (adjust as needed)
    setTimeout(function () {
        document.body.removeChild(errorTooltip);
    }, 3000);
}
