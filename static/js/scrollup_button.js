(function ($) {
    if ($ == undefined) {
        return;
    }

    var html_object;
    var button;

    $(document).ready(function () {
        html_object = $(window);
        append_button();
        button = $('#scrollup_button');
        button.click(function () {
            html_object.scrollTop(0);
            html_object.trigger('scroll');
        });

        $(window).bind('scroll', function () {
            if (html_object.scrollTop() > 268) {
//                button.removeClass('scrl_disabled');
                button.fadeIn();
            }
            else {
//                button.addClass('scrl_disabled');
                button.fadeOut();
            }
        });

        $(window).bind('resize', function () {
            $('#scrollup_button').css('top', top_calc());
        });
    });

    function append_button() {
        $('body').append('<div id="scrollup_button" class="scrl_disabled"></div>');
        $('#scrollup_button').css('top', top_calc());
    }

    function top_calc() {
        return $(window).height() / 2 - 20;
    }

})(jQuery);