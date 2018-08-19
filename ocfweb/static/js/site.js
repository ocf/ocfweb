$(document).ready(function() {
    // sticky footer
    var resizeTimeout;
    var updateFooterHeight = function() {
        var height = $('.ocf-footer').outerHeight();
        $('body').css('margin-bottom', height);
    };

    $(window).on('resize', function() {
        clearTimeout(resizeTimeout);
        setTimeout(updateFooterHeight, 10);
    });

    updateFooterHeight();

    // Close dropdown menu if clicked/tapped outside of
    $(document).on('click', function(event) {
        var menuOpen = $(".navbar-collapse").hasClass("in");

        // If the menu is open and the click occurred somewhere
        //   other than the menu itself, close it.
        if (menuOpen && $('.navbar-collapse').has(event.target).length === 0) {
            $("button.navbar-toggle").trigger('click');
        }
    });
});

// vim: ts=4 sts=4 sw=4
