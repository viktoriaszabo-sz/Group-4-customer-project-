const elements = document.querySelectorAll('p[id]');

elements.forEach(element => {
    const id = element.id;
    fetch(`/get_content/${id}`)
        .then(response => response.json())
        .then(data => {
            element.innerText += data.content;
        })
        .catch(error => console.error('Error:', error));
});