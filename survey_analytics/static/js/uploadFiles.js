let uploadedFiles = [];

const fileInput = document.getElementById('upload-files');
const uploadedFilesContainer = document.getElementById('uploaded-files');

fileInput.addEventListener('change', function(event) {
    handleFiles(event.target.files);
});

function allowDrop(event) {
    event.preventDefault();
}

function handleDrop(event) {
    event.preventDefault();
    const files = event.dataTransfer.files;
    handleFiles(files);
}

function handleFiles(files) {
    for (let i = 0; i < files.length; i++) {
        const file = files[i];
        uploadedFiles.push(file);
        displayFile(file);
    }
    fileInput.value = '';
}

function displayFile(file) {
    const fileItem = document.createElement('div');
    fileItem.className = 'file-item';
    fileItem.innerHTML = `
        <span>
            <img src="${documentIconUrl}" alt="Document Icon" class="icons">
            ${file.name}
        </span>
        <small>${(file.size / (1024 * 1024)).toFixed(1)} mb</small>
        <button type="button" class="remove-file-btn" onclick="removeFile('${file.name}', this)">X</button>
    `;
    uploadedFilesContainer.appendChild(fileItem);
}

function removeFile(fileName, btn) {
    uploadedFiles = uploadedFiles.filter(f => f.name !== fileName);
    const fileItem = btn.parentNode;
    fileItem.parentNode.removeChild(fileItem);
}

function cancelUpload() {
    uploadedFiles = [];
    uploadedFilesContainer.innerHTML = '';
    window.location.href = cancelUrl;
}

const surveyForm = document.querySelector('.survey-form');
surveyForm.addEventListener('submit', function(event) {
});
