function recommend() {
    $.ajax({
         type: 'GET',
         url: 'recommend',
         data: {'real_name': $('#real_name').html()},
         success: function(data) {
             $('#recommendations').empty();
             recommendations = data['recommendations'];
             for (var i in recommendations) {
                 $('#recommendations').append(
                     '<li class="list-group-item list-group-item-success">'+ recommendations[i] +'</li>'
                 );
             }
         }
     });
}
$(document).ready(function() {
    recommend();
});
