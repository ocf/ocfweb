function recommend() {
    $.ajax({
         type: 'GET',
         url: 'recommend',
         data: {'real_name': $('#real_name').html()},
         success: function(data) {
             $('#recommendations').empty();
             for (var i in data) {
                 $('#recommendations').append(
                     '<li class="list-group-item list-group-item-success">'+ data[i] +'</li>'
                 );
             }
         }
     });
}
$(document).ready(function() {
    recommend();
});
