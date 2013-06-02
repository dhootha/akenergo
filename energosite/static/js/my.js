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


function show_modal(modal_id, modal_head, modal_body) {
    if (!modal_id) return;
    $(modal_id).find('.modal-header h3').text(modal_head);
    $(modal_id).find('.modal-body').html(modal_body);
    $(modal_id).modal();
}

function display_form_errors(errors, $form) {
    for (var k in errors) {
        if (errors.hasOwnProperty(k)) {
            $form.find('input[name=' + k + '], select[name=' + k + ']').closest(".control-group").addClass('error');
            $form.find('input[name=' + k + '], select[name=' + k + ']').next(".help-inline").html(errors[k]).fadeIn();
        }
    }
}

function display_non_field_errors(errors, modal_id) {
    if (errors.length == 0) return;
    var result = "<ul> \n";
    for (var i = 0; i < errors.length; i++) result += "<li>" + errors[i] + "</li> \n";
    result += "</ul> \n";
    show_modal(modal_id, 'Ошибка', result);
}

function remove_form_errors($form) {
    $form.find('.control-group').removeClass('error');
    $form.find('.help-inline').hide();
}


function SubmitAjaxForm(form_id, modal_id, modal_head) {
    var $this = $(form_id);
    $this.submit(function (event) {
        event.preventDefault();
        $.ajax({ // create an AJAX call...
//                    context: $this,
            data: $this.serialize(), // get the form data
            type: $this.attr('method'), // GET or POST
            url: $this.attr('action'), // the file to call
            dataType: 'json',
            beforeSend: function (jqXHR, settings) {
                $this.find('input, select').attr('disabled', 'disabled'); // запрещаем редактировать инпуты
                remove_form_errors($this);
//                if (modal_id) $(modal_id).hide();
            },
            success: function (data) { // on success..
                if (data["result"] == 'success') {
                    show_modal(modal_id, modal_head, data["response"]);
//                    if (modal_id) $(modal_id).html(data["response"]).fadeIn();
                }
                else if (data["result"] == 'error') {
                    display_form_errors(data["response"], $this);
                    display_non_field_errors(data["non_f_err"], modal_id);
                }
            },
            complete: function (jqXHR, textStatus) {
                $this.find('input, select').removeAttr('disabled'); // разрешаем редактировать инпуты
            }
        });
    });
}


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
//                if (data["result"] == 'success') {
//                    $('#results').html(data["response"]).fadeIn();
//                }
//                else if (data["result"] == 'error') {
//                    display_form_errors(data["response"], $(this));
//                }
//            },
//            complete: function (jqXHR, textStatus) {
//                $(this).find('input, select').removeAttr('disabled'); // разрешаем редактировать инпуты
//            }
//        });
//        return false;
//    });
});

