document.addEventListener('DOMContentLoaded', () => {
    // Initialize form and elements
    const taskForm = document.getElementById('taskForm');
    const fileInput = document.getElementById('fileInput');
    const dropArea = document.getElementById('dropArea');
    const previewImage = document.getElementById('previewImage');
    const progressContainer = document.getElementById('uploadProgress');
    const progressBar = document.getElementById('progressBar');
    const submittext = document.getElementById('submittext');
    const fullpageLoader = document.getElementById('fullpage-loader');
    const loadertext = document.getElementById('loadertext');

    fullpageLoader.classList.remove('active');

    // Prevent default drag behaviors
    ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
        dropArea.addEventListener(eventName, preventDefaults, false);
    });

    function preventDefaults(e) {
        e.preventDefault();
        e.stopPropagation();
    }

    // Handle dropped files
    dropArea.addEventListener('drop', (e) => {
        const dt = e.dataTransfer;
        const files = dt.files;
        handleFiles(files);
    }, false);

    // Handle file input change
    fileInput.addEventListener('change', () => {
        handleFiles(fileInput.files);
    });

    // Click to trigger file input
    dropArea.addEventListener('click', () => {
        fileInput.click();
    });

    // Process files (preview image)
    function handleFiles(files) {
        const file = files[0];
        if (file && file.type.startsWith('image/')) {
            const reader = new FileReader();
            reader.onload = (e) => {
                previewImage.src = e.target.result;
                previewImage.style.display = 'block';
            };
            reader.readAsDataURL(file);
            // DO NOT attempt to assign to fileInput.files (read-only)
        } else {
            iziToast.error({
                title: 'Error',
                message: 'Please upload a valid image file.',
                position: 'topRight',
                timeout: 5000
            });
            fileInput.value = ''; // Clear invalid file
            previewImage.style.display = 'none';
        }
    }

    // Form submission with Axios
    taskForm.addEventListener('submit', (e) => {
        e.preventDefault();
        const formData = new FormData(taskForm);
        fullpageLoader.classList.add('active');

        // Show progress bar
        progressContainer.style.display = 'block';
        progressBar.style.width = '0%';
        submittext.innerHTML = 'Submitting';
        loadertext.innerHTML = 'Abeg wait small, I dey run your matter';

        const csrfToken = formData.get("csrfmiddlewaretoken");

        axios.post('/studenttask/task_collection', formData, {
            headers: {
                'Content-Type': 'multipart/form-data',
                'X-CSRFToken': csrfToken,
            },
            onUploadProgress: (progressEvent) => {
                const percentCompleted = Math.round((progressEvent.loaded * 100) / progressEvent.total);
                progressBar.style.width = percentCompleted + '%';
                progressBar.setAttribute('aria-valuenow', percentCompleted);
            }
        })
        .then(response => {
            console.log('Success:', response.data);

            iziToast.success({
                title: 'Success',
                message: response.data.success,
                position: 'topRight',
                timeout: 5000
            });

            taskForm.reset();
            previewImage.style.display = 'none';
            progressContainer.style.display = 'none';
            progressBar.style.width = '0%';
            submittext.innerHTML = 'Submit';
            fullpageLoader.classList.remove('active');

            setTimeout(() => {
                window.location.reload();
            }, 1000);
        })
        .catch(error => {
            progressBar.style.width = '0%';
            submittext.innerHTML = 'Submit';
            fullpageLoader.classList.remove('active');

            iziToast.error({
                title: 'Error',
                message: error.response?.data?.error || 'Something went wrong. Please try again.',
                position: 'topRight',
                timeout: 5000
            });
        });
    });
});
