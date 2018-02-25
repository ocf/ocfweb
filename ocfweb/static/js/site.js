$(document).ready(function() {
    // sticky footer
    var resizeTimeout;
    var updateFooterHeight = function() {
        var height = $('.ocf-footer').outerHeight();
        $('body').css('margin-bottom', height);
    };

    $('[data-toogle="tooltip"]').tooltip();

    $(window).resize(function() {
        clearTimeout(resizeTimeout);
        setTimeout(updateFooterHeight, 10);
    });

    updateFooterHeight();

    // Close dropdown menu if clicked/tapped outside of
    $(document).click(function(event) {
        var menuOpen = $(".navbar-collapse").hasClass("in");

        // If the menu is open and the click occurred somewhere
        //   other than the menu itself, close it.
        if (menuOpen && $('.navbar-collapse').has(event.target).length === 0) {
            $("button.navbar-toggle").click();
        }
    });
});
