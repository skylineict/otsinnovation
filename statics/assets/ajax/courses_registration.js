

// Training Mode Description Logic
const trainingDetails = {
  virtual: {
    description:
      "Your classes will be conducted online via Google Meet and Zoom. Access details will be sent to your email.",
    icon: "🖥️",
  },
  physical: {
    description:
      "Classes will be held at Rivers State University - BIO-RSU Innovation Hub.",
    icon: "🏫",
  },
};

const trainingModeSelect = document.querySelectorAll(
  'input[name="trainingMode"]'
);
const trainingInfo = document.getElementById("trainingInfo");

// console.log(trainingModeSelect)
// console.log(trainingInfo)
trainingModeSelect.forEach((radio) => {
  radio.addEventListener("change", function () {
    const selectedMode = this.value;
    

    if (selectedMode && trainingDetails[selectedMode]) {
      const training = trainingDetails[selectedMode];


      trainingInfo.innerHTML = `
            <div class="card border-0">
                <div class="card-body p-0">
                    <div class="d-flex align-items-center mb-2">
                        <span style="font-size: 1.5rem; margin-right: 10px;">${training.icon}</span>
                        <h5 class="card-title mb-0" style="color: #00a86a;">${selectedMode} Training</h5>
                    </div>
                    <p class="card-text p-4">${training.description}</p>
                </div>
            </div>
        `;
      trainingInfo.style.display = "block";
    } else {
      trainingInfo.style.display = "none";
    }
  });
});
// Fetch Course Info & Update Description Box
document.addEventListener("DOMContentLoaded", () => {
  const courseSelect = document.getElementById("course");
  const courseInfo = document.getElementById("courseInfo");
  let courseDetails = {};
 

  axios.get("/courses/fetch_all_courses").then((response) => {
    courseDetails = response.data.courses;
    console


    courseSelect.addEventListener("change", function () {
      const selectedCourseid = this.value;
      const selectedCourse = courseDetails.find(course=> course.id==selectedCourseid)

   
    

     

      if (selectedCourse) {
       
       

                    courseInfo.innerHTML = `
                        <div class="card border-0">
                            <div class="card-body p-0">
                                <h5 class="card-title" style="color: #1b2b5e;">${selectedCourse.name}</h5>
                                <p class="card-text mb-2">${selectedCourse.description}</p>
                                <div class="d-flex align-items-center">
                                    <span class="badge text-white" style="background-color: #1b2b5e; padding: 8px 12px; margin-right: 10px;">Price</span>
                                    <span class="fw-bold">₦${Number(selectedCourse.amount).toLocaleString()}</span>
                                </div>
                                <p class="text-muted small mt-2">*This cost covers all course materials and access to our learning platform.</p>
                            </div>
                        </div>
                    `;
                    courseInfo.style.display = 'block';
                } else {
                    courseInfo.style.display = 'none';
      }
    }); 
  }); 
}); 


document.addEventListener("DOMContentLoaded", () => {
  // Form Validation Logic
  const form = document.getElementById("registrationForm");
  const registrationPage = document.getElementById("registrationPage");
  const loaders = document.getElementById("spinnerOverlay");
  const sucess = document.getElementById("successPage");





  form.addEventListener("submit", function (event) {
    event.preventDefault(); // Prevent the default form submission
    document.getElementById('fullpage-loader').classList.add('active');
    const formData = new FormData(this);

    // Get CSRF token
    const csrfToken = formData.get("csrfmiddlewaretoken");
    console.log(csrfToken);

    axios
      .post("/courses/", formData, {
        headers: {
          "X-CSRFToken": csrfToken,
        },
      })
      .then((response) => {
        document.getElementById('fullpage-loader').classList.remove('active');
        // Check if success key exists in the response
        if (response.data.success) {
          document.getElementById("successCourseName").textContent = response.data.course.name;
          document.getElementById("displayCourseName").textContent = response.data.course.name;
          document.getElementById("successCourseDuration").textContent = response.data.course.duration;
          document.getElementById("displayTrainingMode").textContent = response.data.training_mode;
          document.getElementById("displayInternship").textContent = response.data.internship ? "Yes" : "No";
          document.getElementById("displayFacilitator").textContent = response.data.course.facilitator;
          document.getElementById("displayCourseAmount").textContent = `₦${response.data.course.amount}`;
          document.getElementById("displayStatus").textContent = response.data.is_approved ? "Approved" : "Pending";

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
        document.getElementById('fullpage-loader').classList.remove('active');
        console.log(error.response.data);
        iziToast.error({
            title: "Error",
            message: error.response.data.error,
            position: "topRight",
          });
         
      });
  });
});
