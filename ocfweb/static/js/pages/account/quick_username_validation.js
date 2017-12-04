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
                 if(data.is_valid) {
                     $input.parent().attr('class', 'has-success')
                     $('#valid_username_notif').css('display', 'block');
                     $('#valid_username_notif').text(data.msg);
                     $('#invalid_username_notif').css('display', 'none');

                 } else {
                     $input.parent().attr('class', 'has-error');
                     $('#invalid_username_notif').css('display', 'block');
                     $('#invalid_username_notif').text(data.msg);
                     $('#valid_username_notif').css('display', 'none');
                 }
             }
         });
     }
});
