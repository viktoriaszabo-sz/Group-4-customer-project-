function displaySelectedDiv() {
  // Retrieve the last selected language from localStorage
  var selectedLanguage = localStorage.getItem('selectedLanguage');

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

function changeSelectedLanguage(selectedLanguage) {
  // Store the selected language in localStorage
  localStorage.setItem('selectedLanguage', selectedLanguage);

  // Call the function to display the selected div
  displaySelectedDiv();
}

// Initialize the displayed div based on the initial dropdown value
window.onload = function() {
  displaySelectedDiv();

  // Assuming you have a select element with the id "selectDiv"
  var selectDiv = document.getElementById("selectDiv");

  // Add an event listener to handle changes in the select element
  selectDiv.addEventListener('change', function() {
    changeSelectedLanguage(selectDiv.value);
  });
};
