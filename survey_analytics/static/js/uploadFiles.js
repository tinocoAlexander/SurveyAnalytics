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
    const allowedExtensions = ['csv', 'xls', 'xlsx'];
    for (let i = 0; i < files.length; i++) {
        const file = files[i];
        const ext = file.name.split('.').pop().toLowerCase();

        if (!allowedExtensions.includes(ext)) {
            alert(`The file ${file.name} has an unsupported extension. Allowed extensions are: CSV, XLS, XLSX.`);
            continue;
        }

        if (uploadedFiles.length >= 1) {
            alert("You can only upload one file.");
            continue;
        }

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
    event.preventDefault();

    const surveyNameInput = document.getElementById('survey-name');
    let errors = [];

    if (!surveyNameInput.value.trim()) {
        errors.push("Please, set the name of your survey");
    }

    if (uploadedFiles.length === 0) {
        errors.push("You must upload at least one file");
    }

    if (uploadedFiles.length > 1) {
        errors.push("You can only upload one file");
    }

    if (errors.length > 0) {
        let messagesContainer = document.querySelector('.messages');
        if (!messagesContainer) {
            messagesContainer = document.createElement('div');
            messagesContainer.className = 'messages';
            surveyForm.prepend(messagesContainer);
        }
        messagesContainer.innerHTML = "";
        errors.forEach(error => {
            const messageDiv = document.createElement('div');
            messageDiv.className = 'message error';
            messageDiv.innerText = error;
            messagesContainer.appendChild(messageDiv);
        });
        return;
    }

    const formData = new FormData(surveyForm);
    for (let i = 0; i < uploadedFiles.length; i++) {
        formData.append('upload_files', uploadedFiles[i]);
    }

    fetch(surveyForm.action || window.location.href, {
        method: 'POST',
        body: formData,
        headers: {
            'X-Requested-With': 'XMLHttpRequest'
        }
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        console.log('Success:', data);
        if (data.redirect_url) {
            window.location.href = data.redirect_url;
        } else {
            window.location.reload();
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
});
