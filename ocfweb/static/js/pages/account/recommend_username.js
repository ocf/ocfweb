function recommend() {
    $.ajax({
         type: 'GET',
         url: 'recommend',
         data: {'real_name': $('#real_name').text()},
         success: function(data) {
             $('#recommendations').empty();
             recommendations = data['recommendations'];
             for (var i in recommendations) {
                 $('#recommendations').append(
                     $('<li>')
                         .addClass('list-group-item list-group-item-success')
                         .text(recommendations[i])
                 );
             }
         }
     });
}
$(document).ready(function() {
    recommend();
});
