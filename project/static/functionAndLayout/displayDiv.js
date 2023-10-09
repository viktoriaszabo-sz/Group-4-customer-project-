function displaySelectedDiv() {
    var selectedLanguage = document.getElementById("selectDiv").value;
    var div_fi = document.getElementById("div_fi");
    var div_en = document.getElementById("div_en");

    if (selectedLanguage === "div_fi") {
        div_fi.style.display = "block";
        div_en.style.display = "none";
    } else if (selectedLanguage === "div_en") {
        div_fi.style.display = "none";
        div_en.style.display = "block";
    }
}

// Initialize the displayed div based on the initial dropdown value
window.onload = displaySelectedDiv;