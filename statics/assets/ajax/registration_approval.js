document.addEventListener('DOMContentLoaded', function () {
      const selectAllCheckbox = document.getElementById('select-all');
    const selectedCount = document.getElementById('selected-count');
    const bulkApproveBtn = document.getElementById('bulkApproveButton');
    const bulkDeleteBtn = document.getElementById('bulkDeleteButtton');
    console.log('Bulk Approve Button:', bulkDeleteBtn);
    const registrationTableBody = document.getElementById('registrationTableBody');
    const fullpageLoader = document.getElementById('fullpage-loader');
    const searchInput = document.getElementById('searchInput');
    const filterBtn = document.querySelector('.filter-btn');
    const filterMenu = document.getElementById('filterMenu');
    const paginationContainer = document.querySelector('.pagination-container');

    let currentPage = 1;
    let currentFilter = '';
    let selectedCourseId = '';


      // START: CSRF Token Retrieval
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


       // START: Selection Count Update
    function updateSelectedCount() {
        const selectedCountValue = document.querySelectorAll('input[name="registration_ids"]:checked').length;
        console.log('Selected Count:', selectedCountValue); // Debug
        selectedCount.textContent = selectedCountValue;
        selectedCount.classList.toggle('active', selectedCountValue > 0);
        bulkApproveBtn.disabled = selectedCountValue === 0;
        bulkDeleteBtn.disabled = selectedCountValue === 0;
        console.log('Selected count:', selectedCountValue);
    }


       // START: Empty State Check
    function checkEmptyState() {
        const registrationRows = registrationTableBody.querySelectorAll('tr:not(:has(.empty-state-container))');
        if (registrationRows.length === 0) {
            registrationTableBody.innerHTML = `
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
                            <h3 class="empty-title">No Registrations to Approve</h3>
                        </div>
                    </td>
                </tr>
            `;
            paginationContainer.style.display = 'none';
        }
    }


    
    // START: Table Update
    function updateTable(registrations) {
        registrationTableBody.innerHTML = '';
        if (registrations.length === 0) {
            console.log('No registrations, showing empty state');
            console.log('Registrations:', registrations);
            checkEmptyState();
            return;
        }

        registrations.forEach(reg => {
            console.log(`Rendering row `, reg)
            const row = document.createElement('tr');
            row.innerHTML = `
                <td class="checkbox-col">
                    <label class="custom-checkbox">
                        <input type="checkbox" name="registration_ids" value="${reg.id}">
                        <span class="checkmark"></span>
                    </label>
                </td>
                <td>${reg.full_name || 'N/A'}</td>
                <td>${reg.username}</td>
                <td>${reg.course_name}</td>
                <td>${reg.training_mode}</td>
                <td>
                    <span class="status status-${reg.is_approved ? 'approved' : 'pending'}">${reg.is_approved ? 'Approved' : 'Pending'}</span>
                </td>
                <td>
                    <div class="action-buttons">
                        <button class="btn-action btn-approve single-approve" data-id="${reg.id}" ${reg.is_approved ? 'disabled' : ''}>
                            <i class="fas fa-check"></i> Approve
                        </button>
                        <button class="btn-action btn-delete single-delete" data-id="${reg.id}" ${reg.is_approved ? 'disabled' : ''}>
                            <i class="fas fa-trash"></i> Reject
                        </button>
                    </div>
                </td>
            `;
            registrationTableBody.appendChild(row);
        });

        document.querySelectorAll('input[name="registration_ids"]').forEach(checkbox => {
            checkbox.addEventListener('change', updateSelectedCount);
            console.log('Checkbox added for registration ID:', checkbox.value);
        });

        // attachActionListeners();
    }
    // END: Table Update

    
    // START: Pagination Update
    function updatePagination(pagination) {
        const numbers = document.querySelector('.pagination-numbers');
        numbers.innerHTML = '';

        if (pagination.total_pages <= 0) {
            paginationContainer.style.display = 'none';
            return;
        }

        paginationContainer.style.display = 'flex';
        document.querySelector('.pagination-prev').disabled = !pagination.has_previous;
        document.querySelector('.pagination-next').disabled = !pagination.has_next;

        const maxPagesToShow = 5;
        let startPage = Math.max(1, pagination.current_page - Math.floor(maxPagesToShow / 2));
        let endPage = Math.min(pagination.total_pages, startPage + maxPagesToShow - 1);

        if (endPage - startPage + 1 < maxPagesToShow) {
            startPage = Math.max(1, endPage - maxPagesToShow + 1);
        }

        for (let i = startPage; i <= endPage; i++) {
            const button = document.createElement('button');
            button.className = `pagination-btn pagination-number ${i === pagination.current_page ? 'active' : ''}`;
            button.dataset.page = i;
            button.textContent = i;
            numbers.appendChild(button);
        }

        if (startPage > 1) {
            numbers.insertAdjacentHTML('afterbegin', '<span class="pagination-ellipsis">...</span>');
        }
        if (endPage < pagination.total_pages) {
            numbers.insertAdjacentHTML('beforeend', '<span class="pagination-ellipsis">...</span>');
        }
    }



    // START: Fetch Registrations
    function fetchRegistrations() {
    fullpageLoader.classList.add('active');
    let url = '/admindash/registrations/approve/';
    let params = { page: currentPage };
    console.log('Fetching URL:', url, 'Params:', params, 'Filter:', currentFilter);

    if (currentFilter === 'search') {
        url = '/admindash/registrations/search-approve/';
        const query = searchInput.value.trim();
  
        if (!query) {
            fullpageLoader.classList.remove('active');
            updateTable([]);
            updatePagination({ total_pages: 0, current_page: 1 });
            iziToast.error({
                title: 'Error',
                message: 'Please enter a search term',
                position: 'topRight',
                timeout: 5000
            });
            return;
        }
        params.query = query; // Send single query parameter
    } else if (currentFilter === 'course' && selectedCourseId) {
        url = '/admindash/registrations/filter-by-course/';
        params.course_id = selectedCourseId;
        console.log('Course filter ID:', selectedCourseId); // Debug
    }

    // console.log('Params:', params); // Debug
    axios.get(url, { params: params ,
           headers: { 'X-Requested-With': 'XMLHttpRequest' } // E

    })
 

        .then(response => {
           
            fullpageLoader.classList.remove('active');
            if (response.data.success) {
                updateTable(response.data.student_list);
                updatePagination(response.data.pagination);
               
            
            } else {
                updateTable([]);
                updatePagination({ total_pages: 0, current_page: 1 });
                iziToast.error({
                    title: 'Error',
                    message: response.data.error || 'Search failed',
                    position: 'topRight',
                    timeout: 5000
                });
            }
        })
        .catch(error => {
            fullpageLoader.classList.remove('active');
            updateTable([]);
            updatePagination({ total_pages: 0, current_page: 1 });
            iziToast.error({
                title: 'Error',
                message: error.response?.data?.error || 'Fetch failed',
                position: 'topRight',
                timeout: 5000
            });
        });


}

// Pagination Handler
            paginationContainer.addEventListener('click', (e) => {
                const button = e.target.closest('.pagination-btn');
                if (!button || button.disabled) return;

                e.preventDefault();
                const page = parseInt(button.dataset.page);
                if (!isNaN(page)) {
                    currentPage = page;
                    fetchRegistrations();
                }
            });

// Add click event listener to the filter button
filterBtn.addEventListener('click', () => {
    const isExpanded = filterBtn.getAttribute('aria-expanded') === 'true';

    // Toggle the display of the filter menu
    if (isExpanded) {
        filterMenu.style.display = 'none';
        filterBtn.setAttribute('aria-expanded', 'false');
    } else {
        filterMenu.style.display = 'block'; // Or 'flex', 'grid' if you use flexbox/grid for the menu
        filterBtn.setAttribute('aria-expanded', 'true');
    }
});

//this section fetches the courses and populates the filter menu
axios.get('/admindash/listcourses/')
    .then(response => {
        const courses = response.data.list_courses || [];
        
        courses.forEach(course => {
            const option = document.createElement('a');
            option.className = 'dropdown-item filter-option';
            option.href = '#';
            option.dataset.filter = 'course';
            option.dataset.courseId = course.id;
            option.textContent = course.name || 'Unknown Course';
            filterMenu.appendChild(option);
        });
    });

    // Add click event listener to the filter menu
filterMenu.addEventListener('click', (e) => {
    if (e.target && e.target.classList.contains('filter-option')) {
        e.preventDefault();
        const clickedOption = e.target;
        const courseId = clickedOption.dataset.courseId;

        if (courseId === 'null') {
            currentFilter = '';
            selectedCourseId = '';
        } else {
            currentFilter = 'course';
            selectedCourseId = courseId;
        }

        filterMenu.style.display = 'none'; // Hide menu after selection
        filterBtn.setAttribute('aria-expanded', 'false');
        currentPage = 1;
        fetchRegistrations();
    }
});

// START: Select All Checkbox Handler
    selectAllCheckbox.addEventListener('change', () => {
        const checkboxes = document.querySelectorAll('input[name="registration_ids"]');
        checkboxes.forEach(checkbox => {
            checkbox.checked = selectAllCheckbox.checked;
        });
        updateSelectedCount();
       
    });



   
    // START: Individual Checkbox Handlers
    document.querySelectorAll('input[name="registration_ids"]').forEach(checkbox => {
        checkbox.addEventListener('change', updateSelectedCount);
    });


     // single handles for approval 
        document.querySelectorAll('.single-approval').forEach(button => {
            button.addEventListener('click', () => {
                const registrationId = button.dataset.id;
                const formData = new FormData();
                formData.append('registration_id', registrationId);
                formData.append('action', 'approve');
                formData.append('csrfmiddlewaretoken', getCsrfToken());
                fullpageLoader.classList.add('active');

                axios.post('/admindash/registrations/approve/', formData, {
                    headers: { 'X-CSRFToken': getCsrfToken() }
                })
                    .then(response => {
                        fullpageLoader.classList.remove('active');
                        if (response.data.success) {
                            iziToast.success({
                                title: 'Success',
                                message: response.data.message,
                                position: 'topRight',
                                timeout: 5000
                            });
                            const row = document.querySelector(`input[value="${registrationId}"]`).closest('tr');
                            row.querySelector('.status').textContent = 'Approved';
                            row.querySelector('.status').classList.remove('status-pending');
                            row.querySelector('.status').classList.add('status-approved');
                            row.querySelectorAll('.single-approve, .single-delete').forEach(btn => btn.disabled = true);
                        } else {
                            iziToast.error({
                                title: 'Error',
                                message: response.data.error,
                                position: 'topRight',
                                timeout: 5000
                            });
                        }
                    })
                    .catch(error => {
                        fullpageLoader.classList.remove('active');
                        iziToast.error({
                            title: 'Error',
                            message: error.response?.data?.error || 'Error approving registration.',
                            position: 'topRight',
                            timeout: 6000
                        });
                    });
            });
        });
        //single approval ends here 


        // single handles for rejection
           document.querySelectorAll('.single-rejection').forEach(button => {
            button.addEventListener('click', () => {
                const registrationId = button.dataset.id;
                const formData = new FormData();
                formData.append('registration_id', registrationId);
                formData.append('action', 'reject');
                formData.append('csrfmiddlewaretoken', getCsrfToken());
                fullpageLoader.classList.add('active');

                axios.post('/admindash/registrations/approve/', formData, {
                    headers: { 'X-CSRFToken': getCsrfToken() }
                })
                    .then(response => {
                        fullpageLoader.classList.remove('active');
                        if (response.data.success) {
                            iziToast.success({
                                title: 'Success',
                                message: response.data.message,
                                position: 'topRight',
                                timeout: 5000
                            });
                            const row = document.querySelector(`input[value="${registrationId}"]`).closest('tr');
                            row.classList.add('animate__animated', 'animate__fadeOut');
                            setTimeout(() => {
                                row.remove();
                                checkEmptyState();
                            }, 500);
                        } else {
                            iziToast.error({
                                title: 'Error',
                                message: response.data.error,
                                position: 'topRight',
                                timeout: 6000
                            });
                        }
                    })
                    .catch(error => {
                        fullpageLoader.classList.remove('active');
                        iziToast.error({
                            title: 'Error',
                            message: error.response?.data?.error || 'Error rejecting registration.',
                            position: 'topRight',
                            timeout: 6000
                        });
                    });
            });
        });




          bulkApproveBtn.addEventListener('click', () => {
        const selectedIds = Array.from(document.querySelectorAll('input[name="registration_ids"]:checked')).map(cb => cb.value);

        if (selectedIds.length > 0) {
            const formData = new FormData();
            selectedIds.forEach(id => formData.append('registration_ids[]', id));
            formData.append('action', 'approve');
            formData.append('csrfmiddlewaretoken', getCsrfToken());
            fullpageLoader.classList.add('active');

            axios.post('/admindash/registrations/approve/', formData, {
                headers: { 'X-CSRFToken': getCsrfToken() }
            })
                .then(response => {
                    fullpageLoader.classList.remove('active');
                    if (response.data.success) {
                        iziToast.success({
                            title: 'Success',
                            message: response.data.message,
                            position: 'topRight',
                            timeout: 5000
                        });
                        selectedIds.forEach(id => {
                            const row = document.querySelector(`input[value="${id}"]`).closest('tr');
                             setTimeout(() => {
                                row.remove();
                                checkEmptyState();
                                updateSelectedCount();
                            }, 500);
                            // row.querySelector('.status').textContent = 'Approved';
                            // row.querySelector('.status').classList.remove('status-pending');
                            // row.querySelector('.status').classList.add('status-approved');
                            // row.querySelectorAll('.single-approve, .single-delete').forEach(btn => btn.disabled = true);
                        });
                        selectAllCheckbox.checked = false; 
                        updateSelectedCount();
                    } else {
                        iziToast.error({
                            title: 'Error',
                            message: response.data.error,
                            position: 'topRight',
                            timeout: 5000
                        });
                    }
                })
                .catch(error => {
                    fullpageLoader.classList.remove('active');
                    iziToast.error({
                        title: 'Error',
                        message: error.response?.data?.error || 'Failed to approve registrations.',
                        position: 'topRight',
                        timeout: 5000
                    });
                });
        }
    });



    // START: Bulk Delete Handler
    
    bulkDeleteBtn.addEventListener('click', () => {
        const selectedIds = Array.from(document.querySelectorAll('input[name="registration_ids"]:checked')).map(cb => cb.value);
        if (selectedIds.length > 0) {
            const formsData = new FormData();
            selectedIds.forEach(id => formsData.append('registration_ids[]', id));
            formsData.append('action', 'reject');
            formsData.append('csrfmiddlewaretoken', getCsrfToken());
            fullpageLoader.classList.add('active');

            axios.post('/admindash/registrations/approve/', formsData, formsData, {
                headers: { 'X-CSRFToken': getCsrfToken() }
            })
                .then(response => {
                    fullpageLoader.classList.remove('active');
                    if (response.data.success) {
                        iziToast.success({
                            title: 'Success',
                            message: response.data.message,
                            position: 'topRight',
                            timeout: 5000
                        });
                        selectedIds.forEach(id => {
                            const row = document.querySelector(`input[value="${id}"]`).closest('tr');
                            row.classList.add('animate__animated', 'animate__fadeOut');
                            
                            setTimeout(() => {
                                row.remove();
                                 updateSelectedCount();
                                checkEmptyState();
                            }, 500);
                        });
                        selectAllCheckbox.checked = false;
                        updateSelectedCount();
                    } else {
                        iziToast.error({
                            title: 'Error',
                            message: response.data.error,
                            position: 'topRight',
                            timeout: '5000'
                        });
                    }
                })
                .catch(error => {
                    fullpageLoader.classList.remove('active');
                    iziToast.error({
                        title: 'Error',
                        message: error.response?.data?.error || 'Failed to reject registrations.',
                        position: 'topRight',
                        timeout: 6000
                    });
                });
        }
    });
    // END: Bulk Actions


 

  



 
            // Debounce Utility
            function debounce(func, wait) {
                let timeout;
                return function executedFunction(...args) {
                    const later = () => {
                        clearTimeout(timeout);
                        func(...args);
                    };
                    clearTimeout(timeout);
                    timeout = setTimeout(later, wait);
                };
            }

    // START: Search Input Handler
    searchInput.addEventListener('input', debounce(() => {
        const query = searchInput.value.trim();
        if (query.length < 3 && query.length > 0) return;
       // Set search filter
        currentFilter = query ? 'search' : '';
        selectedCourseId = '';
        currentPage = 1;
        fetchRegistrations();
    }, 500));

 // Initial Setup
            updateSelectedCount();
});