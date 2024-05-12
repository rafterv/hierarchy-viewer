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

        // Update HTML file hyperlink
        if (data.download_html) {
            document.getElementById('htmlLink').href = data.download_html;
        }
        
        // Construct download links
        if (data.success) {

            
            var magjacLink = document.createElement('a');
            magjacLink.href = data.download_magjac;
            magjacLink.textContent = 'Hierarchy Editor';
            magjacLink.target = '_blank';
            document.getElementById('results').appendChild(magjacLink);

            var downloadJsonLink = document.createElement('a');
            downloadJsonLink.href = data.download_json;
            downloadJsonLink.textContent = 'Download JSON';
            downloadJsonLink.download = 'generated_file.json';
            document.getElementById('results').appendChild(downloadJsonLink);

            // Display PNG image on the page
            var pngImage = document.createElement('img');
            pngImage.src = data.download_png;
            pngImage.style.maxWidth = '100%'; // Ensure the image fits within its container
            pngImage.style.height = 'auto'; // Maintain aspect ratio
            pngImage.style.maxHeight = '400px'; // Limit the maximum height of the image
            document.getElementById('results').appendChild(pngImage);

            var downloadPngLink = document.createElement('a');
            downloadPngLink.href = data.download_png;
            downloadPngLink.textContent = 'Download PNG';
            downloadPngLink.download = 'generated_file.png';
            document.getElementById('results').appendChild(downloadPngLink);
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
});