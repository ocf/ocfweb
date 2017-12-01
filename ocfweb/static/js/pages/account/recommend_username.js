function recommend() {
    $.ajax({
         type: 'GET',
         url: 'recommend',
         data: {'real_name': $('#real_name').text()},
         success: function(data) {
             $('#recommendations').empty();
             var recommendations = data['recommendations'];
             for (var i in recommendations) {
                 var recommendation = recommendations[i];
                 $('#recommendations').append(
                     $('<button>', {
                         type: 'button',
                         class: 'list-group-item list-group-item-success',
                         onclick: '$("#id_ocf_login_name").val("' + recommendation + '").trigger("keyup");',
                         text: recommendation
                     })
                 );
             }
         }
     });
}
$(document).ready(function() {
    recommend();
});
