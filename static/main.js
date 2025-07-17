document.addEventListener('DOMContentLoaded', function() {
    const dropZone = document.getElementById('dropZone');
    const fileInput = document.getElementById('fileInput');
    const loadingSpinner = document.getElementById('loadingSpinner');
    const errorAlert = document.getElementById('errorAlert');
    const successAlert = document.getElementById('successAlert');
    const downloadBtn = document.getElementById('downloadBtn');

    dropZone.addEventListener('dragover', (e) => {
        e.preventDefault();
        dropZone.style.borderColor = '#4299e1';
        dropZone.style.background = '#ebf8ff';
    });
    dropZone.addEventListener('dragleave', (e) => {
        e.preventDefault();
        dropZone.style.borderColor = '#cbd5e0';
        dropZone.style.background = '#f7fafc';
    });
    dropZone.addEventListener('drop', (e) => {
        e.preventDefault();
        dropZone.style.borderColor = '#cbd5e0';
        dropZone.style.background = '#f7fafc';
        const files = e.dataTransfer.files;
        if (files.length > 0) {
            handleFile(files[0]);
        }
    });
    fileInput.addEventListener('change', (e) => {
        if (e.target.files.length > 0) {
            handleFile(e.target.files[0]);
        }
    });
    function handleFile(file) {
        if (!file.name.endsWith('.docx')) {
            showError('请上传 .docx 格式的文件');
            return;
        }
        const formData = new FormData();
        formData.append('file', file);
        loadingSpinner.style.display = 'block';
        errorAlert.style.display = 'none';
        successAlert.style.display = 'none';
        downloadBtn.style.display = 'none';
        fetch('/upload', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            loadingSpinner.style.display = 'none';
            if (data.success) {
                successAlert.style.display = 'block';
                downloadBtn.style.display = 'inline-block';
            } else {
                showError(data.error || '处理文件时发生错误');
            }
        })
        .catch(error => {
            loadingSpinner.style.display = 'none';
            showError('上传文件时发生错误');
        });
    }
    function showError(message) {
        errorAlert.textContent = message;
        errorAlert.style.display = 'block';
        successAlert.style.display = 'none';
        downloadBtn.style.display = 'none';
    }
    downloadBtn.addEventListener('click', () => {
        window.location.href = '/download';
    });
});
