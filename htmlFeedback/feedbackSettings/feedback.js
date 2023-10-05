// Define categories, response numbers, and languages
const categories = [1, 2, 3, 4, 5, 6, 7, 8];
//const responseNumbers = [3, 3, 3, 3, 3, 3, 3, 3];
const responseNumbers = [2, 2, 2, 2, 2, 2, 2, 2];
//const responseNumbers = [1, 1, 1, 1, 1, 1, 1, 1];
const lang = 'en'; // the selected language

// Function to construct the file name
function constructFileName(category, responseNumber, lang) {
    return (100 * category + responseNumber) + '_' + lang + '.txt'; // Constructs a filename
}

// Function to read file content
function readFile(category, responseNumber) {
    const fileName = constructFileName(category, responseNumber, lang); // Constructs the filename
    const filePath = './paragraphsResponse/' + fileName; // Constructs the file path

    fetch(filePath) // Fetches the file
        .then(response => {
            if (!response.ok) {
                throw new Error('Network Response Error'); // Throws an error if network response is not ok
            }
            return response.text(); // Returns the response text
        })
        .then(text => {
            displayFileContent('category ' + category, text); // Displays the file content
        })
        .catch(error => console.error('Error:', error)); // Handles errors
}

// Function to display file content with line breaks
function displayFileContent(elementId, content) {
    const displaying = document.getElementById(elementId); // Gets the HTML element by ID
    displaying.innerHTML = '<strong>The content of ' + elementId + ' is the following:</strong><br>' + content.replace(/\n/g, '<br>'); // Displays the content
}

// Loop through categories and display content
for (let i = 0; i < categories.length; i++) {
    const category = categories[i]; // Gets the current category
    const responseNumber = responseNumbers[i]; // Gets the corresponding response number
    readFile(category, responseNumber); // Reads and displays file content for the current category
}