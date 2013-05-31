/**
 * Created with PyCharm.
 * User: manjaro
 * Date: 31.05.13
 * Time: 13:30
 * To change this template use File | Settings | File Templates.
 */


function PrintWindow() {
    window.print();
    setTimeout("window.close();", 300);
}

function display_form_errors(errors, $form) {
    for (var k in errors) {
        if (errors.hasOwnProperty(k)) {
            $form.find('input[name=' + k + '], select[name=' + k + ']').closest(".control-group").addClass('error');
            $form.find('input[name=' + k + '], select[name=' + k + ']').next(".help-inline").html(errors[k]).fadeIn();
        }
    }
}

function remove_form_errors($form) {
    $form.find('.control-group').removeClass('error');
    $form.find('.help-inline').hide();
}


(function ($) {
    jQuery.fn.SubmitAjaxForm = function (results_id, ajax_mess_id, ajax_message) {
        return this.each(function () {
            var $this = $(this);
            $this.submit(function (event) {
                event.preventDefault();
                // Your function goes here
                $.ajax({ // create an AJAX call...
//                    context: $this,
                    data: $this.serialize(), // get the form data
                    type: $this.attr('method'), // GET or POST
                    url: $this.attr('action'), // the file to call
                    dataType: 'json',
                    beforeSend: function (jqXHR, settings) {
                        $this.find('input, select').attr('disabled', 'disabled'); // запрещаем редактировать инпуты
                        remove_form_errors($this);
                        if (results_id) $(results_id).hide();
                        if (ajax_mess_id) $(ajax_mess_id).parent().addClass("hide");
                    },
                    success: function (data) { // on success..
                        if (data.result == 'success') {
                            if (results_id) $(results_id).html(data.response).fadeIn();
                            if (ajax_mess_id) {$(ajax_mess_id).parent().removeClass("hide");
                                $(ajax_mess_id).html(ajax_message);
                            }
                        }
                        else if (data.result == 'error') {
                            display_form_errors(data.response, $this);
                            if (ajax_mess_id) $(ajax_mess_id).parent().addClass("hide");
                        }
                    },
                    complete: function (jqXHR, textStatus) {
                        $this.find('input, select').removeAttr('disabled'); // разрешаем редактировать инпуты
                    }
                });

            });
        });
    };
})(jQuery);


$(function () {
    $('div.input-required > input, div.input-required > textarea, div.input-required > select').attr('required', '');
    $('a[data-toggle=tooltip]').tooltip();
    $("a[data-toggle=popover], button[data-toggle=popover]").popover({ trigger: "hover focus", delay: 100 });


//    $('#standard_form').submit(function () {
//        $.ajax({ // create an AJAX call...
//            context: $('#standard_form'),
//            data: $(this).serialize(), // get the form data
//            type: $(this).attr('method'), // GET or POST
//            url: $(this).attr('action'), // the file to call
//            dataType: 'json',
//            beforeSend: function (jqXHR, settings) {
//                $(this).find('input, select').attr('disabled', 'disabled'); // запрещаем редактировать инпуты
//                remove_form_errors($(this));
//                $('#results').hide();
//            },
//            success: function (data) { // on success..
//                if (data.result == 'success') {
//                    $('#results').html(data.response).fadeIn();
//                }
//                else if (data.result == 'error') {
//                    display_form_errors(data.response, $(this));
//                }
//            },
//            complete: function (jqXHR, textStatus) {
//                $(this).find('input, select').removeAttr('disabled'); // разрешаем редактировать инпуты
//            }
//        });
//        return false;
//    });
});

