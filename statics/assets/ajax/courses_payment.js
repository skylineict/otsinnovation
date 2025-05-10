document.addEventListener('DOMContentLoaded', () => {
  const paymentForm = document.getElementById('paymentForm');
  const amountToPayInput = document.getElementById('amountToPay');
  const fullPaymentRadio = document.getElementById('fullPayment');
  const partialPaymentRadio = document.getElementById('installmentPayment');
  const bankTransferRadio = document.getElementById('bankTransfer');
  const automaticPaymentRadio = document.getElementById('automaticPayment');
  const bankSelection = document.getElementById('bankSelection');
  const paymentModal = $('#paymentModal');
  const fullpageLoader = document.getElementById('fullpage-loader');
    let pollingInterval = null; // To store polling interval



  // Function to format the amount with currency symbol
  const formatAmount = (amount) => `₦${parseFloat(amount).toFixed(2)}`;

   // Function to format payment mode for display
    const formatPaymentMode = (mode) => {
        if (mode === 'banktransfer' || mode === 'bank_transfer') return 'Bank Transfer';
        if (mode === 'virtualaccount') return 'Virtual Account';
        return 'Unknown';
    };

  // Function to update the amount to pay
const updateAmountToPay = () => {
        // Get the selected payment option
        const selectedOption = paymentForm.querySelector('input[name="paymentOption"]:checked');
        if (selectedOption) {
            const amount = selectedOption.value;
            // Update amountToPay input, keeping ₦ for display
            amountToPayInput.value = formatAmount(amount);
        }
    
    };

    // Show/hide bank selection
    const toggleBankSelection = () => {
      bankSelection.style.display = bankTransferRadio.checked ? 'block' : 'none';
  };

      // Initialize
      updateAmountToPay();
      toggleBankSelection();

  // Add event listeners to radio buttons
  [fullPaymentRadio, partialPaymentRadio].forEach(radio => {
      radio.addEventListener('change', () => {
          // Update amount asynchronously
          setTimeout(() => {
              updateAmountToPay();
          }, 0);
      });
  });


  // Add event listener to bank transfer radio button
  [bankTransferRadio, automaticPaymentRadio].forEach(radio => {
    radio.addEventListener('change', toggleBankSelection);
    
});


 function startCountdown(expirationTime) {
        const expirationDate = new Date(expirationTime);
        if (isNaN(expirationDate)) {
            console.error('Invalid expiration time:', expirationTime);
            // Fallback to 15 minutes if expiration time is invalid
            expirationDate = new Date(Date.now() + 15 * 60 * 1000);
        }

        const countdownElement = document.getElementById('countdownTimer');

        const interval = setInterval(function () {
            const now = new Date();
            const timeLeft = (expirationDate - now) / 1000; // Seconds remaining

           if (timeLeft <= 0) {
                clearInterval(interval);
                clearInterval(pollingInterval); // Stop polling
                countdownElement.textContent = "EXPIRED";
                paymentModal.modal('hide');
                iziToast.warning({
                    title: "Expired",
                    message: "The virtual account has expired. Please try again.",
                    position: "topRight"
                });
                return;
            }
            const minutes = Math.floor(timeLeft / 60);
            const seconds = Math.floor(timeLeft % 60);

            countdownElement.textContent =
                (minutes < 10 ? "0" + minutes : minutes) +
                ":" +
                (seconds < 10 ? "0" + seconds : seconds);

            if (timeLeft <= 300 && timeLeft > 60) {
                countdownElement.classList.add("timer-warning"); // Yellow for <5 min
            } else if (timeLeft <= 60) {
                countdownElement.classList.remove("timer-warning");
                countdownElement.classList.add("timer-danger"); // Red for <1 min
            }
        }, 1000);
    }



    // / Polling function to check payment status
    function startPolling(paymentId, timerInterval) {
        const verifyUrl = document.querySelector('.modal-body a[href*="verify_payment"]').href; // Reuse 
      console.log("Polling URL:", verifyUrl);
        // verify_payment URL
        pollingInterval = setInterval(() => {
            axios
                .post(verifyUrl, {}, {
                    headers: {
                        "X-CSRFToken": document.querySelector('input[name="csrfmiddlewaretoken"]').value
                    }
                })
                .then((response) => {
                    const data = response.data;
                    if (data.status === 'success') {
                        // Payment approved: stop timer and polling, redirect
                        clearInterval(timerInterval);
                        clearInterval(pollingInterval);
                        paymentModal.modal('hide');
                        iziToast.success({
                            title: "Success",
                            message: "Payment confirmed automatically!",
                            position: "topRight"
                        });
                        setTimeout(() => {
                            window.location.href = data.redirect_url;
                        }, 1500);
                    } else if (data.status === 'failed' || data.status === 'error') {
                        // Payment failed: stop polling, show error
                        clearInterval(pollingInterval);
                        paymentModal.modal('hide');
                        iziToast.error({
                            title: data.status === 'failed' ? "Failed" : "Error",
                            message: data.error,
                            position: "topRight"
                        });
                        setTimeout(() => {
                            window.location.href = data.redirect_url;
                        }, 1500);
                    }
                    // Continue polling for 'pending' status
                })
                .catch((error) => {
                    console.error('Polling error:', error);
                    // Continue polling on error to avoid stopping prematurely
                });
        }, 5000); // Poll every 5 seconds
    }


    paymentForm.addEventListener('submit', function (event) {
        event.preventDefault(); // Prevent default form submission
        console.log("Form submitted");
        fullpageLoader.classList.add('active'); // Show loader
        const formData = new FormData(this);
        const amountValue = amountToPayInput.value.replace('₦', '').trim();
        formData.set('amountToPay', amountValue);
        console.log("Form amountToPay:", amountValue);
        console.log("paymentOption:", formData.get('paymentOption'),formData.get('paymentMethod') );

        const csrfToken = formData.get("csrfmiddlewaretoken");
            // Client-side validation
        if (!formData.get('paymentOption') || !formData.get('paymentMethod') || !amountValue) {
            fullpageLoader.classList.remove('active');
            iziToast.error({
                title: "Error",
                message: "All fields are required.",
                position: "topRight"
            });
            return;
        }
        if (formData.get('paymentMethod') === 'bank' && !formData.get('bankCode')) {
            fullpageLoader.classList.remove('active');
            iziToast.error({
                title: "Error",
                message: "Bank selection is required for bank transfer.",
                position: "topRight"
            });
            return;
        }
        
        axios
            .post(window.location.href, formData, {
                headers: {
                    "X-CSRFToken": csrfToken,
                },
            }).then((response) => {
                console.log("Response:", response.data);
                fullpageLoader.classList.remove('active'); // Hide loader
                  if (response.data.success) {
                    const data = response.data.data;
                    document.getElementById('modalBankName').textContent = data.account_bank || data.virtual_account_bank;
                    document.getElementById('accountNumber').textContent = data.account_number || data.virtual_account_number;
                    document.getElementById('accountName').textContent = data.account_name || data.virtual_account_name;
                    document.getElementById('modalAmount').textContent = formatAmount(data.amount);
                    document.getElementById('modalPaymentMode').textContent = formatPaymentMode(data.mode);

                    const paymentId = document.querySelector('.modal-body a[href*="verify_payment"]').href.split('/').slice(-2)[0]; // Extract payment_id
                    console.log("Payment ID:", paymentId);

                    if (data.account_expiration) {
                        startCountdown(data.account_expiration, paymentId);
                    } else {
                        startCountdown(new Date(Date.now() + 15 * 60 * 1000).toString(), paymentId);
                    }

                    // ✅ Start polling here
                      startPolling(paymentId); // No need to pass interval

                    paymentModal.modal('show');

                    iziToast.success({
                        title: "Success",
                        message: "Virtual account created successfully. Please make the payment before the account expires.",
                        position: "topRight"
                    });
                }
            })
            
            .catch((error) => {
                fullpageLoader.classList.remove('active'); // Hide loader
                console.error(error.response.data);
                // NEW: Show error toast
                // Purpose: Displays an error notification using iziToast if the API request fails, showing the server’s error message or a generic fallback.
                iziToast.error({
                    title: "Error",
                    message: error.response.data.error || "An error occurred. Please try again.",
                    position: "topRight"
                });
            });
       

    });

        // Copy account number button
    document.getElementById('copyAccountBtn').addEventListener('click', () => {
        const accountNumber = document.getElementById('accountNumber').textContent;
        navigator.clipboard.writeText(accountNumber).then(() => {
            iziToast.info({
                title: "Copied",
                message: "Account number copied to clipboard!",
                position: "topRight"
            });
        });
    });

    });

    



          
          
      