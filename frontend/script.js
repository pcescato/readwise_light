document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('upload-form');
    const fileInput = document.getElementById('file-input');
    const fileInputLabel = document.getElementById('file-input-label');
    const submitButton = document.getElementById('submit-button');
    const loader = document.getElementById('loader');
    const errorMessage = document.getElementById('error-message');
    const resultsContainer = document.getElementById('results');
    const summaryContent = document.getElementById('summary-content');
    const keywordsList = document.getElementById('keywords-list');

    fileInput.addEventListener('change', () => {
        if (fileInput.files.length > 0) {
            fileInputLabel.textContent = fileInput.files[0].name;
        } else {
            fileInputLabel.textContent = 'Choisir un fichier...';
        }
    });

    form.addEventListener('submit', async (event) => {
        event.preventDefault();

        const file = fileInput.files[0];
        if (!file) {
            showError('Veuillez sélectionner un fichier.');
            return;
        }

        // Reset UI
        hideError();
        resultsContainer.classList.add('hidden');
        loader.classList.remove('hidden');
        submitButton.disabled = true;

        const formData = new FormData();
        formData.append('file', file);

        try {
            const response = await fetch('http://194.146.25.179:8000/extract', {
                method: 'POST',
                body: formData,
            });

            if (!response.ok) {
                const errorData = await response.json().catch(() => ({ detail: 'Erreur inconnue du serveur.' }));
                throw new Error(errorData.detail || `Erreur HTTP: ${response.status}`);
            }

            const data = await response.json();
            displayResults(data);

        } catch (error) {
            showError(error.message);
        } finally {
            loader.classList.add('hidden');
            submitButton.disabled = false;
        }
    });

    function displayResults(data) {
        // Display Summary
        summaryContent.textContent = data.summary || 'Aucun résumé disponible.';

        // Display Keywords
        keywordsList.innerHTML = '';
        if (data.keywords && data.keywords.length > 0) {
            data.keywords.forEach(keyword => {
                const pill = document.createElement('span');
                pill.className = 'keyword-pill';
                pill.textContent = keyword;
                keywordsList.appendChild(pill);
            });
        } else {
            const noKeyword = document.createElement('p');
            noKeyword.textContent = 'Aucun mot-clé extrait.';
            keywordsList.appendChild(noKeyword);
        }

        resultsContainer.classList.remove('hidden');
    }

    function showError(message) {
        errorMessage.textContent = message;
        errorMessage.classList.remove('hidden');
    }

    function hideError() {
        errorMessage.classList.add('hidden');
    }
});
