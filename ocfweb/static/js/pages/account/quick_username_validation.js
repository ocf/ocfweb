$(document).ready(function() {
    var finTypingCountdown = 250; // 250 milliseconds
    var typingTimer;
    var $input = $('#id_ocf_login_name');

    // On keyup, start countdown
    $input.keyup(function() {
        clearTimeout(typingTimer);
        typingTimer = setTimeout(validate_username, finTypingCountdown);
    });

    // On keydown, clear countdown
    $input.keydown(function() {
        clearTimeout(typingTimer);
    });

    function validate_username() {
        $.ajax({
             type: 'GET',
             url: 'validate',
             data: {'username': $input.val(),
                    'real_name': $('#real_name').text()},
             success: function(data) {
                 var $username_feedback = $('#username_feedback')
                 if(data.is_valid) {
                    $input.parent().removeClass('has-error')
                                   .addClass('has-success');
                    $username_feedback.removeClass('alert-danger')
                                      .addClass('alert-success');
                 } else {
                    $input.parent().removeClass('has-success')
                                   .addClass('has-error');
                    $username_feedback.removeClass('alert-sucess')
                                      .addClass('alert-danger');
                 }
                 $username_feedback.show().text(data.msg);
             }
         });
     }
});
