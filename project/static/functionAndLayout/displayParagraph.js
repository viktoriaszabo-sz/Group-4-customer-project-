function displayParagraph(id) {
    const element = document.getElementById(id); // Select the specific <p> element with the given ID
    
    fetch(`/get_content/${id}`)
        .then(response => response.json())
        .then(data => {
            element.innerText = data.content;
        })
        .catch(error => console.error('Error:', error));
}