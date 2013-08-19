/**
 * Created with PyCharm.
 * User: manjaro
 * Date: 31.05.13
 * Time: 13:30
 * To change this template use File | Settings | File Templates.
 */

//(function ($) {
//    if ($ == undefined) {
//        return;
//    }

function myPrintWindow() {
    window.print();
    setTimeout("window.close();", 300);
}

function mySortDict(dict) {
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


function myShowModal(modal_header, modal_body) {
    var $this = $("#ajax_results");
    $this.find('.modal-header h4').text(modal_header);
    if (!modal_body)
        $this.find('.modal-body').hide();
    else
        $this.find('.modal-body').show().html(modal_body);
    $this.modal();
//        .css({'margin-top': ($(window).height() - $this.height()) / 2, 'top': 0});
}


function myClearForm($form) {
    $form.find('.control-group').removeClass('error');
    $form.find('.help-inline').empty();
    $form.find('#ajax_non_field_errors').remove();
    $form.find('#ajax_form_success').remove();
}

function myScrollPage(selector, step) {
    if ($(selector).length)
        $('html, body').animate({scrollTop: $(selector).offset().top - step}, 'fast');
    return false;
}


function myShowFormSuccess($form, header, body) {
    var html = '<div id="ajax_form_success" class="alert alert-success alert-block">' +
        '<button type="button" class="close" data-dismiss="alert">&times;</button>';
    if (header) html += '<h4>' + header + '</h4>';
    html += body +
        '</div>';
    $form.prepend(html);
}


function myDisplayNonfieldError($form, error) {
    var html = '<div id="ajax_non_field_errors" class="alert alert-error alert-block">' +
        '<button type="button" class="close" data-dismiss="alert">&times;</button>' +
        error +
        '</div>';
    var find1 = $form.find('.form-actions:last');
    var find2 = $form.find('.control-group:last');
    if (find1.length)
        find1.before(html);
    else if (find2.length)
        find2.before(html);

}

function myDisplayFormErrors($form, errors) {
    for (var k in errors) if (errors.hasOwnProperty(k)) {
        $form.find('input[name=' + k + '], textarea[name=' + k + '], select[name=' + k + ']').closest(".control-group").addClass('error');
        $form.find('input[name=' + k + '], textarea[name=' + k + '], select[name=' + k + ']').closest(".control-group").find('.help-inline').text(errors[k]);
        if (k === 'captcha') {
            $form.find('input[name=captcha_1]').closest(".control-group").addClass('error');
            $form.find('input[name=captcha_1]').closest(".control-group").find('.help-inline').text(errors[k]);
        }
        if (k === 'non_field') {
            myDisplayNonfieldError($form, errors[k]);
        }
    }
}

function myUpdateValues(values) {
    for (var key in values) if (values.hasOwnProperty(key)) {
        $('#' + key).text(values[key]);
    }
}

function mySubmitAjaxForm(form_selector) {
    var $this = $(form_selector);
    $this.submit(function (event) {
        event.preventDefault();
        $.ajax({ // create an AJAX call...
//                    context: $this,
            data: $this.serialize(), // get the form data
            type: $this.attr('method'), // GET or POST
            url: $this.attr('action'), // the file to call
            dataType: 'json',
            timeout: 60000,
            beforeSend: function (jqXHR, settings) {
                $this.find('input, select').attr('disabled', true); // запрещаем редактировать инпуты
                $this.css("visibility", 'hidden');
                $('footer').css("visibility", 'hidden');

                myClearForm($this);
            },
            error: function (jqXHR, textStatus, errorThrown) {
                myDisplayNonfieldError($this, "ERROR: " + errorThrown);
            },
            success: function (data, textStatus, jqXHR) {
                if (data["captcha_key"] && data["captcha_image"]) {
                    $this.find("img.captcha").attr('src', data["captcha_image"]);
                    $this.find('#id_captcha_0').val(data["captcha_key"]);
                    $this.find('#id_captcha_1').val('');
                }
                if (data["result"] === 'success') {
                    myUpdateValues(data["update_values"]);
                    if (data['success_in_modal'])
                        myShowModal(data['response_header'], data["response_body"]);
                    else {
                        myShowFormSuccess($this, data['response_header'], data["response_body"]);
                        myScrollPage("#ajax_form_success", 55);
                    }

                }
                else if (data["result"] === 'error') {
                    myDisplayFormErrors($this, data["errors"]);
                }
            },
            complete: function (jqXHR, textStatus) {
                $this.css("visibility", 'visible');
                $('footer').css("visibility", 'visible');
                $this.find('input, select').removeAttr('disabled'); // разрешаем редактировать инпуты
            }
        });
    });
}


//$(function () {


//    $('#standard_form').submit(function () {
//        $.ajax({ // create an AJAX call...
//            context: $('#standard_form'),
//            data: $(this).serialize(), // get the form data
//            type: $(this).attr('method'), // GET or POST
//            url: $(this).attr('action'), // the file to call
//            dataType: 'json',
//            beforeSend: function (jqXHR, settings) {
//                $(this).find('input, select').attr('disabled', 'disabled'); // запрещаем редактировать инпуты
//                myClearForm($(this));
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
//});

//})(jQuery);