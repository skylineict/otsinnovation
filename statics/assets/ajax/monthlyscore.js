document.addEventListener("DOMContentLoaded", function () { 

    const modal = document.getElementById("createRequirementModal");
    const loader = document.getElementById("fullpage-loader");
    const courseSelect = document.getElementById("course_id");
     const approveButtons = document.querySelectorAll('.approve-score');
    const rejectButtons = document.querySelectorAll('.reject-score');

    

    // const trap = bootstrap.Modal.getInstance(modal) || new bootstrap.Modal(modal);


 $(modal).on("show.bs.modal", function () {
        loader.classList.add("active");


        
        $.ajax({
            url:'/monthlyscore/api/courses/',
            type: "GET",
            dataType: "json",
            success: function (response) {
                loader.classList.remove("active");

                if (response.success) {
                    courseSelect.innerHTML = '<option value="">Select a course</option>';
                    response.courses.forEach(function (course) {
                        const option = document.createElement("option");
                        option.value = course.id;
                        option.textContent = course.name;
                        courseSelect.appendChild(option);
                    });
                
                }
            },
            error: function (xhr) {
                loader.classList.remove("active");
                console.log(xhr.responseJSON || xhr);
                iziToast.error({
                    title: "Error",
                    message: "Failed to fetch courses. Please try again.",
                    position: "topRight",
                });
            }
        });


        
        

 });

const form = document.getElementById("requirementForm");

if (form) {
       form.addEventListener("submit", function (event) {
        event.preventDefault();
        loader.classList.add("active");

        const formData = new FormData(form);
        const csrfToken = formData.get("csrfmiddlewaretoken");

        axios
            .post("/monthlyscore/monthly-requirement/", formData, {
                headers: {
                    "X-CSRFToken": csrfToken,
                },
            })
            .then((response) => {
                loader.classList.remove("active");

                if (response.data.success) {
                    // Hide modal and reset form
                  $('#createRequirementModal').modal('hide');
                    form.reset();

                    iziToast.success({
                        title: "Success",
                        message: response.data.message,
                        position: "topRight",
                    });
                } else {
                    iziToast.error({
                        title: "Error",
                        message: response.data.error || "Failed to create requirement.",
                        position: "topRight",
                    });
                }
            })
            .catch((error) => {
                loader.classList.remove("active");
                console.log(error.response ? error.response.data : error);
                iziToast.error({
                    title: "Error",
                    message: error.response?.data?.error || "An error occurred. Please try again.",
                    position: "topRight",
                });
            });
    });

    
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




    // Handle approve button clicks
        // Handle approve button clicks
    approveButtons.forEach(button => {
        button.addEventListener('click', function () {
            const requirementId = this.getAttribute('data-id');
            loader.classList.add("active");
            const csrfmiddlewaretoken = getCsrfToken();

            // Create form data
            const formData = new FormData();
            formData.append('requirement_id', requirementId);
            formData.append('action', 'approve');

            axios({
                method: "post",
                url: '/monthlyscore/approve-requirement/',
                data: formData,
                headers: {
                    'X-CSRFToken': csrfmiddlewaretoken
                }
            }).then(response => {
                loader.classList.remove('active');

                if (response.data.success) {
                    // Remove the row from the table
                    document.getElementById(`requirement-${requirementId}`).remove();
                    iziToast.success({
                        title: 'Success',
                        message: response.data.message,
                        position: 'topRight'
                    });

                    // Check if table is empty
                    if (!document.querySelector('tbody tr')) {
                        document.querySelector('tbody').innerHTML = `
                            <tr>
                                <td colspan="5">
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
                                        <h3 class="empty-title">No Pending Score Requirements</h3>
                                    </div>
                                </td>
                            </tr>
                        `;
                    }
                }
            }).catch(error => {
                loader.classList.remove('active');
                console.log(error.response.data || error);
                iziToast.error({
                    title: 'Error',
                    message: error.response.data?.error || 'An error occurred. Please try again.',
                    position: 'topRight'
                });
            });
        });
    });
    // Handle reject button clicks



})
