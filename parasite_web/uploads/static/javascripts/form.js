const fileLabel = document.getElementById('file-label');

// Change input name
function handleFileUpload(input) {
    if (input.files.length > 0) {
        fileLabel.textContent = input.files[0].name;
    } else {
        fileLabel.textContent = 'Browse image';
    }
}