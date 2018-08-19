function validate_username() {
    var $username_field = $('#id_ocf_login_name'),
        $username_feedback = $('#username-feedback');
    $.ajax({
         type: 'GET',
         url: 'validate/',
         data: {'username': $username_field.val(),
                'real_name': $('#real-name').text()},
         success: function(data) {
             if(data.is_valid) {
                $username_field.parent().removeClass('has-error')
                               .addClass('has-success');
                $username_feedback.removeClass('alert-danger')
                                  .addClass('alert-success');
             } else {
                $username_field.parent().removeClass('has-success')
                               .addClass('has-error');
                $username_feedback.removeClass('alert-sucess')
                                  .addClass('alert-danger');
             }
             $username_feedback.show().text(data.msg);
         }
     });
 }

function recommend() {
    $.ajax({
         type: 'GET',
         url: 'recommend',
         data: {'real_name': $('#real-name').text()},
         success: function(data) {
             $('#recommendations').empty();
             var recommendations = data['recommendations'];
             for (var i in recommendations) {
                 var recommendation = recommendations[i];
                 $('#recommendations').append(
                     // Generate a new element like this to avoid minification
                     // errors with yui-compressor
                     $($.parseHTML('<button></button>'))
                         .text(recommendation)
                         .attr('type', 'button')
                         .addClass('list-group-item list-group-item-action list-group-item-success recommendation')
                         .on('click', function() {
                             $("#id_ocf_login_name").val($(this).text()).trigger("keyup");
                         })
                 );
             }
         }
     });
}


$(document).ready(function() {
    // Quick validation of username field
    var finTypingCountdown = 250; // 250 milliseconds
    var typingTimer;
    var $input = $('#id_ocf_login_name');

    // On keyup, start countdown
    $input.on('keyup', function() {
        clearTimeout(typingTimer);
        typingTimer = setTimeout(validate_username, finTypingCountdown);
    });

    // On keydown, clear countdown
    $input.on('keydown', function() {
        clearTimeout(typingTimer);
    });

    // Load in recommendations
    recommend();
});

// vim: ts=4 sts=4 sw=4
