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

function sortDict(dict) {
    var keys = [];
    for (var i in dict)
        if (dict.hasOwnProperty(i))
            keys.push(i);
    keys.sort();
    var sortedArray = [];
    for (var j = 0; j < keys.length; j++) {
        sortedArray[keys[j]] = dict[keys[j]];
    }
    return sortedArray;
}


function show_modal(modal_id, modal_head, modal_body) {
    if (!modal_id) return;
    var $this = $(modal_id);
    $this.find('.modal-header h3').text(modal_head);
    if (!modal_body)
        $this.find('.modal-body').hide();
    else
        $this.find('.modal-body').show().html(modal_body);
    $this.modal().css({'margin-top': ($(window).height() - $this.height()) / 2 + 'px', 'top': '0'});
}

function display_form_errors($form, errors) {
    for (var k in errors) if (errors.hasOwnProperty(k)) {
        $form.find('input[name=' + k + '], textarea[name=' + k + '], select[name=' + k + ']').closest(".control-group").addClass('error');
        $form.find('input[name=' + k + '], textarea[name=' + k + '], select[name=' + k + ']').closest(".control-group").find('.help-inline').text(errors[k]);
        if (k === 'captcha') {
            $form.find('input[name=captcha_1]').closest(".control-group").addClass('error');
            $form.find('input[name=captcha_1]').closest(".control-group").find('.help-inline').text(errors[k]);

        }
        if (k === 'non_field')
            $form.find('#ajax_non_field_errors').text(errors[k]).show();

    }
}

function update_values($form, values) {
    for (var key in values) if (values.hasOwnProperty(key)) {
        $('#'+key).text(values[key]);
    }
}

function display_errors_tt(modal_id, modal_head, errors) {

    if (errors.length == 0) return;
    var result = '<table class="table-hover table table-bordered"> \n';
//    result+= '<tr><th></th><th></th></tr>'

    for (var k in sortDict(errors)) {
        if (errors.hasOwnProperty(k)) {
            result += '<tr> \n <th>' + k + '</th> \n <td>' + errors[k] + '</td> \n </tr> \n';
        }
    }
    result += "</table>";
    show_modal(modal_id, modal_head, result);
}

function remove_form_errors($form) {
    $form.find('.control-group').removeClass('error');
    $form.find('.help-inline').empty();
    $form.find('#ajax_non_field_errors').hide();
}


function SubmitAjaxForm(form_id, modal_id, complete_func) {
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
//                $this.hide();
                $this.css("visibility", 'hidden');
                remove_form_errors($this);
            },
            success: function (data) { // on success..
                if (data["captcha_key"] && data["captcha_image"]) {
                    $this.find("img.captcha").attr('src', data["captcha_image"]);
                    $this.find('#id_captcha_0').val(data["captcha_key"]);
                    $this.find('#id_captcha_1').val('');
                }

                if (data["result"] === 'success') {
                    update_values($this, data["update_values"]);
                    show_modal(modal_id, data['response_header'], data["response"]);
                }
                else if (data["result"] === 'error') {
                    display_form_errors($this, data["errors"]);
                }
            },
            complete: function (jqXHR, textStatus) {
//                $this.fadeIn('fast');
                $this.css("visibility", 'visible');
                $this.find('input, select').removeAttr('disabled'); // разрешаем редактировать инпуты
            }
        });
    });
}


$(function () {
//    $('div.input-required > input, div.input-required > textarea, div.input-required > select').attr('required', '');
    $('a[data-toggle=tooltip]').tooltip();
    $("a[data-toggle=popover], button[data-toggle=popover]").popover({ trigger: "hover focus", delay: 127 });


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
//                    display_errors(data["response"], $(this));
//                }
//            },
//            complete: function (jqXHR, textStatus) {
//                $(this).find('input, select').removeAttr('disabled'); // разрешаем редактировать инпуты
//            }
//        });
//        return false;
//    });
});

