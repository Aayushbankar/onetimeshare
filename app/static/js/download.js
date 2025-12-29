const downloadBtn = document.getElementById('download-button');

if (downloadBtn) {
    downloadBtn.addEventListener('click', () => {
        const token = downloadBtn.dataset.token;
        window.location.href = `/d/${token}`;
    });
}

    
