// function to read the file
function readFile(elementId, filePath) {
    fetch(filePath) // Fetches the file
    .then(response => {
        if (!response.ok) {
            throw new Error('Network Response Error'); // Throws an error if network response is not ok
        }
        return response.text(); // Returns the response text
    })
    .then(text => {
        displayFileContent(elementId, text); // Displays the file content
    })
    .catch(error => console.error('Error:', error)); // Handles errors
}

// Function to display file content with line breaks
function displayFileContent(elementId, content) {
    const displaying = document.getElementById(elementId); // Gets the HTML element by ID
    displaying.innerHTML =  content.replace(/\n/g, '<br>'); // Displays the content
}
