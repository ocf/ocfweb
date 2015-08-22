$(document).ready(function() {
    // sticky footer
    // TODO: can we do this with affix?
    // http://getbootstrap.com/javascript/#affix
    var resizeTimeout;
    var updateFooterHeight = function() {
        var height = $('.ocf-footer').height();
        console.log(height);
    };

    $(window).resize(function() {
        clearTimeout(resizeTimeout);
        setTimeout(updateFooterHeight, 1);
    });

    updateFooterHeight();
});
