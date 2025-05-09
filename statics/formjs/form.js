$(document).ready(function(){
    $('#username').change(function(){
      const username = $('#username').val();
      $.ajax({

        url: "reg/usernamevalide",
        data: {
          'username':  username
        },

        dataType: 'json',

        success: function(data){

          if (data.is_taken){
            swal("sorry!", "username already Registered!", "error");
          }

}
});
  
});
  
  });
  