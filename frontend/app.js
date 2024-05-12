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
        // Clear previous results
        document.getElementById('results').innerHTML = '';

        // Update HTML file hyperlink
        if (data.download_html) {
            document.getElementById('htmlLink').href = data.download_html;
        }
        
        // Construct download links
        if (data.success) {

            // Add space between upload button and download links
            var spacer = document.createElement('div');
            spacer.style.height = '20px'; // Adjust height as needed
            document.getElementById('results').appendChild(spacer);

            //MagJac Editor
            var magjacLink = document.createElement('a');
            magjacLink.href = data.download_magjac;
            magjacLink.textContent = 'Editor';
            magjacLink.target = '_blank';
            magjacLink.style.marginRight = '40px'; // Add right margin to separate from other links
            document.getElementById('results').appendChild(magjacLink);
            
            // JSON Download
            var downloadJsonLink = document.createElement('a');
            downloadJsonLink.href = data.download_json;
            downloadJsonLink.textContent = 'Download JSON';
            downloadJsonLink.download = 'generated_file.json';
            downloadJsonLink.style.marginRight = '40px'; // Add right margin to separate from other links
            document.getElementById('results').appendChild(downloadJsonLink);
            
            // PNG Download
            var downloadPngLink = document.createElement('a');
            downloadPngLink.href = data.download_png;
            downloadPngLink.textContent = 'Download PNG';
            downloadPngLink.download = 'generated_file.png';
            downloadPngLink.style.marginRight = '40px'; // Add right margin to separate from other links
            document.getElementById('results').appendChild(downloadPngLink);

            // Add space between upload button and download links
            var spacer = document.createElement('div');
            spacer.style.height = '20px'; // Adjust height as needed
            document.getElementById('results').appendChild(spacer);

            // Insert line break before appending PNG image
            document.getElementById('results').appendChild(document.createElement('br'));


            // Display PNG image on the page
            var pngImage = document.createElement('img');
            pngImage.src = data.download_png;
            pngImage.style.maxWidth = '100%'; // Ensure the image fits within its container
            pngImage.style.height = 'auto'; // Maintain aspect ratio
            pngImage.style.maxHeight = '400px'; // Limit the maximum height of the image
            document.getElementById('results').appendChild(pngImage);
            
            // Insert line break
            document.getElementById('results').appendChild(document.createElement('br'));

            // Add space between upload button and download links
            var spacer = document.createElement('div');
            spacer.style.height = '20px'; // Adjust height as needed
            document.getElementById('results').appendChild(spacer);

            // Embed HTML file in an iframe
            var htmlIframe = document.createElement('iframe');
            htmlIframe.src = data.download_html;
            htmlIframe.width = '50%';
            htmlIframe.height = '600';
            document.getElementById('results').appendChild(htmlIframe);


        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
});