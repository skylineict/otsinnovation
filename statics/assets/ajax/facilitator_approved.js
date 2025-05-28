

document.addEventListener("DOMContentLoaded", function () {
    const approveButtons = document.querySelectorAll('.approve-btn');
    const rejectButtons = document.querySelectorAll('.reject-btn');
    const loader = document.getElementById("fullpage-loader");


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

     
    // console.log("Approve button:", approveButtons);
    // console.log("Reject button:", rejectButtons);


      // Handle approve button clicks
   approveButtons.forEach(button => {
        button.addEventListener('click', function () {
             const registrationId = this.getAttribute('data-id');
             loader.classList.add("active");
              csrfmiddlewaretoken = getCsrfToken()

        // Create form data
            const formData = new FormData();
            formData.append('registration_id', registrationId);
            formData.append('action', 'approve')
              
              

                   axios 
                .post('/facilitator/facilitator_approval', 
                    formData, {
                    headers: {
                        'X-CSRFToken':csrfmiddlewaretoken
                    }
                }).then(response => {
                    loader.classList.remove('active');
                 
                    if (response.data.success) {
                        // Remove the row from the table
                        document.getElementById(`registration-${registrationId}`).remove();
                        iziToast.success({
                            title: 'Success',
                            message: response.data.success,
                            position: 'topRight'
                        });


                          if (!document.querySelector('tbody tr')) {
                        document.querySelector('tbody').innerHTML = `
                            <tr>
                                <td colspan="4">
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
                                        <h3 class="empty-title">No Pending Facilitator Applications</h3>
                                    </div>
                                </td>
                            </tr>
                        `;
                    }

                    };




                      })
                      
                      .catch(error => {
                   loader.classList.remove('active');
                
                    iziToast.error({
                        title: 'Error',
                        message: error.response.data.error || 'An error occurred. Please try again.',
                        position: 'topRight'
                    });
                });


                          
             

        });
        });




    // Handle reject button clicks
    
    
   rejectButtons.forEach(button => {
        button.addEventListener('click', function () {
             const registrationId = this.getAttribute('data-id');
             loader.classList.add("active");
              csrfmiddlewaretoken = getCsrfToken()

        // Create form data
            const formData = new FormData();
            formData.append('registration_id', registrationId);
            formData.append('action', 'reject')
              
              

                   axios 
                .post('/facilitator/facilitator_approval', 
                    formData, {
                    headers: {
                        'X-CSRFToken':csrfmiddlewaretoken
                    }
                }).then(response => {
                    loader.classList.remove('active');
                 
                    if (response.data.success) {
                        // Remove the row from the table
                        document.getElementById(`registration-${registrationId}`).remove();
                        iziToast.success({
                            title: 'Success',
                            message: response.data.success,
                            position: 'topRight'
                        });


                          if (!document.querySelector('tbody tr')) {
                        document.querySelector('tbody').innerHTML = `
                            <tr>
                                <td colspan="4">
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
                                        <h3 class="empty-title">No Pending Facilitator Applications</h3>
                                    </div>
                                </td>
                            </tr>
                        `;
                    }

                    };




                      })
                      
                      .catch(error => {
                   loader.classList.remove('active');
                
                    iziToast.error({
                        title: 'Error',
                        message: error.response.data.error || 'An error occurred. Please try again.',
                        position: 'topRight'
                    });
                });


                          
             

        });
        });

});