$(document).ready(function() {
    // sticky footer
    var resizeTimeout;
    var updateFooterHeight = function() {
        var height = $('.ocf-footer').outerHeight();
        $('body').css('margin-bottom', height);
    };

    $(window).resize(function() {
        clearTimeout(resizeTimeout);
        setTimeout(updateFooterHeight, 10);
    });

    updateFooterHeight();
});
