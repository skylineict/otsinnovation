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

  console.log('Payment form loaded:', paymentForm);
  console.log('Amount to pay input:', amountToPayInput);
  console.log('Full payment radio:', fullPaymentRadio);
  console.log('Installment payment radio:', partialPaymentRadio);


  // Function to format the amount with currency symbol
  const formatAmount = (amount) => `₦${parseFloat(amount).toFixed(2)}`;

  // Function to update the amount to pay
  const updateAmountToPay = () => {
      const selectedOption = paymentForm.querySelector('input[name="paymentOption"]:checked') || fullPaymentRadio;
      const amount = selectedOption.value;
      amountToPayInput.value = formatAmount(amount);
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
    console.log('Bank transfer radio button:', bankTransferRadio);
});
});
          
          
          
          
          
          
          // // Proceed to Payment button in form
          //  $("#proceedToPaymentBtn").click(function () {
          //   // Show modal with virtual account
          //   $("#paymentModal").modal("show");
  
          //   // Set amount in modal
          //   $("#modalAmount").text($("#amountToPay").val());
  
          //   // Start countdown
          //   startCountdown(15 * 60); // 15 minutes in seconds
          // });
  
          // // Copy account number
          // $("#copyAccountBtn").click(function () {
          //   const accountNumber = $("#accountNumber").text();
          //   navigator.clipboard.writeText(accountNumber).then(function () {
          //     $("#copyAccountBtn")
          //       .attr("title", "Copied!")
          //       .tooltip("_fixTitle")
          //       .tooltip("show");
          //     setTimeout(function () {
          //       $("#copyAccountBtn")
          //         .attr("title", "Copy Account Number")
          //         .tooltip("_fixTitle");
          //     }, 1500);
          //   });
          // });
  
          // // Timer functionality
          // function startCountdown(duration) {
          //   let timer = duration;
          //   const countdownElement = document.getElementById("countdownTimer");
  
          //   const interval = setInterval(function () {
          //     const minutes = Math.floor(timer / 60);
          //     const seconds = timer % 60;
  
          //     countdownElement.textContent =
          //       (minutes < 10 ? "0" + minutes : minutes) +
          //       ":" +
          //       (seconds < 10 ? "0" + seconds : seconds);
  
          //     // Add warning classes based on time remaining
          //     if (timer <= 300 && timer > 60) {
          //       // 5 minutes to 1 minute
          //       countdownElement.classList.add("timer-warning");
          //     } else if (timer <= 60) {
          //       // Less than 1 minute
          //       countdownElement.classList.remove("timer-warning");
          //       countdownElement.classList.add("timer-danger");
          //     }
  
          //     if (--timer < 0) {
          //       clearInterval(interval);
          //       countdownElement.textContent = "EXPIRED";
          //       // Here you could add code to handle expiration
          //     }
          //   }, 1000);
          // }
      