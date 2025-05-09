$("#login-form").on("submit", function (e) {
  e.preventDefault();
  const $form = $(this);
  const $btn = $("#btn-login");
  const $spinner = $(".spinner-border");
  const $btntext = $("#btn-text");

  $spinner.show();
  $btn.prop("disabled", true).css({
    "background-color": "#8361eb", // Change button color
    cursor: "not-allowed", // Disable cursor
  });
  $btntext.text("login..");
  const csrftoken = $("[name=csrfmiddlewaretoken]").val();
 

  $.ajax({
    type: "POST",
    url: "/reg/login",
    data: $form.serialize(),
    dataType: "json",
    headers: {
      "X-CSRFToken": csrftoken
    },

    success: function (res) {
if (res.profile) {
    iziToast.success({
        title: "Success",
        message: res.profile,
        position: "topRight",
      });

      setTimeout(function() {
        window.location.href = res.redirect_url;
    }, 2000);
}



// else if (res.task){
//   iziToast.success({
//     title: "Success",
//     message: res.task,
//     position: "topRight",
//   });

//   setTimeout(function() {
//     window.location.href = res.redirect_url;
// }, 3000);
//   }



//   else if (res.unapproved){
//     iziToast.success({
//       title: "Success",
//       message: res.unapproved,
//       position: "topRight",
//     });
  
//     setTimeout(function() {
//       window.location.href = res.redirect_url;
//   }, 3000);
//     } 
    
    
    
    else{
      iziToast.success({
        title: "Success",
        message: res.success,
        position: "topRight",
      });
    
      setTimeout(function() {
        window.location.href = res.redirect_url;
    }, 3000);


    }


  



$form[0].reset();
      $spinner.hide();
      $btn.prop("disabled", false).css({
        "background-color": "",
        cursor: "",
      });

      $btntext.text("proceed");
    
    },

    error: function (eror) {
      iziToast.error({
        title: "Error",
        message: eror.responseJSON.error,
        position: "topRight",
      });
    
      $spinner.hide();
      $btn.prop("disabled", false).css({
        "background-color": "",
        cursor: "",
      });

      $btntext.text("proceed");

      
    },


  });
});
