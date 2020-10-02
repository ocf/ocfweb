$(function(){
    // If the menu is open and the click occurred somewhere
    //   other than the menu itself, close it.
    $(document).on('click', event => {
        const menuOpen = $('.navbar-collapse');
        if (menuOpen.hasClass('in') && menuOpen.has(event.target).length === 0) {
            $('button.navbar-toggle').trigger('click');
        }
    })
})

// vim: ts=4 sts=4 sw=4
