document.addEventListener("DOMContentLoaded", function () {

    const form = document.getElementById("facilitatorform");
    const registrationPage = document.getElementById("registration-page");
     const loader = document.getElementById("fullpage-loader");
      const successPage = document.getElementById("successPage");
      
   

     console.log("Form:", form);

     form.addEventListener("submit", function (event) {

        event.preventDefault(); // Prevent the default form submission
        // Show the loader
        loader.classList.add("active");

        const formData = new FormData(form);
        const csrfToken = formData.get("csrfmiddlewaretoken");
       
        axios
            .post("/facilitator/", formData, {
                headers: {
                    "X-CSRFToken": csrfToken,
                },
            }).then((response) => {
               
                if (response.data.success) {
                  loader.classList.remove("active");
                   // Show success page and hide form
                  successPage.style.display = "block";
                   registrationPage.style.display = "none";
                   
                  

                    iziToast.success({
                        title: "Success",
                        message: response.data.success,
                        position: "topRight",
                    });
                }
            })
            .catch((error) => {
                 loader.classList.remove("active");
               
                console.log(error.response.data);
                iziToast.error({
                    title: "Error",
                    message: error.response.data.error || "An error occurred. Please try again.",
                    position: "topRight",
                });
            });

  });

        
    
});
