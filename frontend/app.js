// frontend/app.js
document.getElementById('uploadForm').addEventListener('submit', function(event) {
    event.preventDefault();
    var formData = new FormData();
    formData.append('file', document.getElementById('fileInput').files[0]);

    fetch('/upload', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        // Display results or handle response as needed
        document.getElementById('results').innerText = JSON.stringify(data);
    })
    .catch(error => {
        console.error('Error:', error);
    });
});
