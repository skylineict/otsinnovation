console.log("ir is wieiifivivi");

$("#registration-form").on("submit", function (e) {
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
  $btntext.text("waiting");
  var csrftoken = $("[name=csrfmiddlewaretoken]").val();
  console.log(csrftoken)

  $.ajax({
    type: "POST",
    url: "/reg/",
    data: $form.serialize(),
    dataType: "json",
    headers: {
      "X-CSRFToken": csrftoken,
    },

    success: function (res) {
      if (res.success) {
        iziToast.success({
          title: "Success",
          message: res.success,
          position: "topRight",
        });

        setTimeout(function () {
          window.location.href = res.redirect;
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
