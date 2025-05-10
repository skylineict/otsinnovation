document.addEventListener('DOMContentLoaded', () => {
    // NEW: Handle payment verification
    // Purpose: Send an AJAX request to the verify_payment endpoint when the user clicks "I've Made the Payment",
    // process JSON responses (success, pending, failed, error), display iziToast messages, and redirect as needed.
    const verifyButton = document.querySelector('.modal-body a[href*="verify_payment"]');
    const paymentModal = $('#paymentModal');
    const fullpageLoader = document.getElementById('fullpage-loader');

    if (verifyButton) {
        verifyButton.addEventListener('click', function (event) {
            event.preventDefault(); // Prevent default navigation
            const verifyUrl = this.href;
            fullpageLoader.classList.add('active'); // Show loader

            axios
                .post(verifyUrl, {}, {
                    headers: {
                        "X-CSRFToken": document.querySelector('input[name="csrfmiddlewaretoken"]').value
                    }
                })
                .then((response) => {
                    fullpageLoader.classList.remove('active'); // Hide loader
                    const data = response.data;

                    if (data.status === 'success') {
                        // NEW: Handle successful verification
                        // Purpose: Show success message, hide modal, and redirect to my-courses
                        iziToast.success({
                            title: "Success",
                            message: data.message,
                            position: "topRight"
                        });
                        paymentModal.modal('hide');
                        setTimeout(() => {
                            window.location.href = data.redirect_url;
                        }, 1500); // Delay redirect for toast visibility
                    } else if (data.status === 'pending') {
                        // NEW: Handle pending verification
                        // Purpose: Inform user to retry later, keep modal open for retry
                        iziToast.info({
                            title: "Pending",
                            message: data.message,
                            position: "topRight"
                        });
                    } else if (data.status === 'failed' || data.status === 'error') {
                        // NEW: Handle failed or error verification
                        // Purpose: Show error message, hide modal, and redirect to appropriate page
                        iziToast.error({
                            title: data.status === 'failed' ? "Failed" : "Error",
                            message: data.error,
                            position: "topRight"
                        });
                        paymentModal.modal('hide');
                        setTimeout(() => {
                            window.location.href = data.redirect_url;
                        }, 1500); // Delay redirect for toast visibility
                    }
                })
                .catch((error) => {
                    fullpageLoader.classList.remove('active');
                    // NEW: Handle HTTP errors (400, 403, 500)
                    // Purpose: Display error message for network issues or server errors
                    console.error('Verification error:', error.response ? error.response.data : error);
                    const errorMessage = error.response && error.response.data.error
                        ? error.response.data.error
                        : "Failed to verify payment. Please try again.";
                    iziToast.error({
                        title: "Error",
                        message: errorMessage,
                        position: "topRight"
                    });
                    if (error.response && error.response.data.redirect_url) {
                        paymentModal.modal('hide');
                        setTimeout(() => {
                            window.location.href = error.response.data.redirect_url;
                        }, 1500);
                    }
                });
        });
    }
});