document.addEventListener('DOMContentLoaded', function () {
    // Initialize form and elements
      // Initialize elements
    const selectAllCheckbox = document.getElementById('select-all');
    const selectedCount = document.getElementById('selected-count');
    const bulkApproveBtn = document.getElementById('bulkApproveBtn');
    const bulkDeleteBtn = document.getElementById('bulkDeleteBtn');
    const taskTableBody = document.getElementById('taskTableBody');
    const fullpageLoader = document.getElementById('fullpage-loader');

    console.log(fullpageLoader);

       selectAllCheckbox.addEventListener('change', () => {
        const checkboxes = document.querySelectorAll('input[name="task_collection_ids"]');
      
        checkboxes.forEach(cb => {
            console.log(cb);
            cb.checked = selectAllCheckbox.checked;
        });
        updateSelectedCount()
        ;});

    document.querySelectorAll('input[name="task_collection_ids"]').forEach(checkbox => {
        checkbox.addEventListener('change', updateSelectedCount);
    });


        function updateSelectedCount() {
        const selectedCountValue = document.querySelectorAll('input[name="task_collection_ids"]:checked').length;
        selectedCount.textContent = selectedCountValue;
        selectedCount.classList.toggle('active', selectedCountValue > 0);
        bulkApproveBtn.disabled = selectedCountValue === 0;
        bulkDeleteBtn.disabled = selectedCountValue === 0;
    }


        // CSRF token retrieval
    function getCsrfToken() {
        const name = 'csrftoken';
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

// / Single approval
    document.querySelectorAll('.single-approve').forEach(button => {
        button.addEventListener('click', () => {
            console.log(button)
            const taskId = button.dataset.id;
            const formData = new FormData();
            formData.append('task_collection_id', taskId);
            console.log(taskId);
            formData.append('csrfmiddlewaretoken', getCsrfToken());
              fullpageLoader.classList.add('active');

              
        axios.post('/studenttask/task_approved', formData, {
            headers: {
                'X-CSRFToken': getCsrfToken()
            },
            
        })
           .then(response => {
                if (response.data.success) {
                    iziToast.success({
                        title: 'Success',
                        message: response.data.message,
                        position: 'topRight',
                        timeout: 5000
                    });
                    fullpageLoader.classList.remove('active');
                    const row = document.querySelector(`input[value="${taskId}"]`).closest('tr');
                    row.classList.add('animate__animated', 'animate__fadeOut');
                    setTimeout(() => {
                        row.remove();
                        checkEmptyState();
                    }, 500);
                }
            })

             .catch(error => {
                iziToast.error({
                    title: 'Error',
                    message: error.response?.data?.error || 'Something went wrong. Please try again.',
                    position: 'topRight',
                    timeout: 5000
                });

                fullpageLoader.classList.remove('active');
            })

        
           


        })

    });
           


    
    // Bulk approval
    bulkApproveBtn.addEventListener('click', () => {
        const selectedIds = Array.from(document.querySelectorAll('input[name="task_collection_ids"]:checked')).map(cb => cb.value);
        console.log(selectedIds);

        if (selectedIds.length) {
            const formData = new FormData();
            selectedIds.forEach(id => formData.append('task_collection_ids[]', id));
            formData.append('csrfmiddlewaretoken', getCsrfToken());
            fullpageLoader.classList.add('active');

           axios.post('/studenttask/task_approved', formData, {
            headers: {
                'X-CSRFToken': getCsrfToken()
            },
            })
            .then(response => {
                if (response.data.success) {
                    iziToast.success({
                        title: 'Success',
                        message: response.data.message,
                        position: 'topRight',
                        timeout: 5000
                    });
                    fullpageLoader.classList.remove('active');
                    selectedIds.forEach(id => {
                        const row = document.querySelector(`input[value="${id}"]`).closest('tr');
                        row.classList.add('animate__animated', 'animate__fadeOut');
                        setTimeout(() => {
                            row.remove();
                            checkEmptyState();
                        }, 500);
                    });
                    selectAllCheckbox.checked = false;
                    updateSelectedCount();
                }
            })
            .catch(error => {
                iziToast.error({
                    title: 'Error',
                    message: error.response?.data?.error || 'Something went wrong. Please try again.',
                    position: 'topRight',
                    timeout: 5000
                });
                fullpageLoader.classList.remove('active');
            })
         
        }
    });



// / Single deletion
    document.querySelectorAll('.single-delete').forEach(button => {
        button.addEventListener('click', () => {
            console.log(button)
            const taskId = button.dataset.id;
            const formData = new FormData();
            formData.append('task_collection_id', taskId);
            console.log(taskId);
            formData.append('csrfmiddlewaretoken', getCsrfToken());
              fullpageLoader.classList.add('active');

              
        axios.post('/studenttask/task_delete', formData, {
            headers: {
                'X-CSRFToken': getCsrfToken()
            },
            
        })
           .then(response => {
                if (response.data.success) {
                    iziToast.success({
                        title: 'Success',
                        message: response.data.message,
                        position: 'topRight',
                        timeout: 5000
                    });
                    fullpageLoader.classList.remove('active');
                    const row = document.querySelector(`input[value="${taskId}"]`).closest('tr');
                    row.classList.add('animate__animated', 'animate__fadeOut');
                    setTimeout(() => {
                        row.remove();
                        checkEmptyState();
                    }, 500);
                }
            })

             .catch(error => {
                iziToast.error({
                    title: 'Error',
                    message: error.response?.data?.error || 'Something went wrong. Please try again.',
                    position: 'topRight',
                    timeout: 5000
                });

                fullpageLoader.classList.remove('active');
            })

        
           


        })

    });


     
    // Bulk deletion 
    bulkDeleteBtn.addEventListener('click', () => {
        const selectedIds = Array.from(document.querySelectorAll('input[name="task_collection_ids"]:checked')).map(cb => cb.value);
        console.log(selectedIds);

        if (selectedIds.length) {
            const formData = new FormData();
            selectedIds.forEach(id => formData.append('task_collection_ids[]', id));
            formData.append('csrfmiddlewaretoken', getCsrfToken());
            fullpageLoader.classList.add('active');

           axios.post('/studenttask/task_delete', formData, {
            headers: {
                'X-CSRFToken': getCsrfToken()
            },
            })
            .then(response => {
                if (response.data.success) {
                    iziToast.success({
                        title: 'Success',
                        message: response.data.message,
                        position: 'topRight',
                        timeout: 5000
                    });
                    fullpageLoader.classList.remove('active');
                    selectedIds.forEach(id => {
                        const row = document.querySelector(`input[value="${id}"]`).closest('tr');
                        row.classList.add('animate__animated', 'animate__fadeOut');
                        setTimeout(() => {
                            row.remove();
                            checkEmptyState();
                        }, 500);
                    });
                    selectAllCheckbox.checked = false;
                    updateSelectedCount();
                }
            })
            .catch(error => {
                iziToast.error({
                    title: 'Error',
                    message: error.response?.data?.error || 'Something went wrong. Please try again.',
                    position: 'topRight',
                    timeout: 5000
                });
                fullpageLoader.classList.remove('active');
            })
         
        }




    });

   // Check for empty state
    function checkEmptyState() {
        const taskRows = taskTableBody.querySelectorAll('tr:not(:has(.empty-state-container))');
        if (taskRows.length === 0) {
            taskTableBody.innerHTML = `
                <tr>
                    <td colspan="7">
                        <div class="empty-state-container">
                            <div class="illustration-container">
                                <div class="empty-box"></div>
                                <i class="search-icon fas fa-search"></i>
                                <i class="document-icon fas fa-file-alt"></i>
                                <div class="dots">
                                    <div class="dot"></div>
                                    <div class="dot"></div>
                                    <div class="dot"></div>
                                </div>
                            </div>
                            <h3 class="empty-title">No Tasks   to Approve</h3>
                        </div>
                    </td>
                </tr>
            `;
        }
    }


// Initialize
    updateSelectedCount();
   




});