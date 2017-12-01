$(document).ready(function() {
    var finTypingCountdown = 250; // 250 milliseconds
    var typingTimer;
    var $input = $('#id_ocf_login_name');

    // On keyup, start countdown
    $input.keyup(function() {
        //alert('key UP');
        clearTimeout(typingTimer);
        typingTimer = setTimeout(validate_username, finTypingCountdown);
    });

    // On keydown, clear countdown
    $input.keydown(function() {
        //alert('key DOWN');
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
                     $input.css('border', '5px solid #3c763d');
                     $('#valid_username_notif').css('display', 'block');
                     $('#valid_username_notif').text(data.msg);
                     $('#invalid_username_notif').css('display', 'none');

                 } else {
                     $input.css('border', '5px solid #a94442');
                     $('#invalid_username_notif').css('display', 'block');
                     $('#invalid_username_notif').text(data.msg);
                     $('#valid_username_notif').css('display', 'none');
                 }
             }
         });
     }
});
