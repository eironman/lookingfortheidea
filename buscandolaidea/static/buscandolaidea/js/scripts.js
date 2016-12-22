$(document).on('ready', function() {
    $('.mobile_menu_icon').on('click', function() {
        $("nav").toggle();
    });
    $('.more_intro').on('click', function() {
        $(".intro span").show();
        $(this).hide();
    });
});