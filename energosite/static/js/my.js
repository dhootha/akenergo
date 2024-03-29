/**
 * Created with PyCharm.
 * User: manjaro
 * Date: 31.05.13
 * Time: 13:30
 * To change this template use File | Settings | File Templates.
 */

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


function myShowDatasInModal(data) {
    var $dialog_modal = $("#ajax_results");
    $dialog_modal.find('.modal-header h4').text(data['response_header']);
    if (!data["response_body"])
        $dialog_modal.find('.modal-body').hide();
    else
        $dialog_modal.find('.modal-body').show().html(data["response_body"]);
    $dialog_modal.modal();
//        .css({'margin-top': ($(window).height() - $dialog_modal.height()) / 2, 'top': 0});
}

function myModalAjaxForm(link_selector, modal_selector) {
    $(link_selector).click(function (e) {
                e.preventDefault();
                $('.modal-body-body', modal_selector).empty();
                var $link = $(this);
                var $url = $(this).attr('data-formurl');
                $.getJSON($url, function (data) {
                    $('.modal-title', modal_selector).text($link.text());
                    $('.modal-body-form', modal_selector).html(data['form']);
                    mySubmitAjaxForm(modal_selector+' form', 'datas', modal_selector+ ' .modal-body-body', false);
                    $(modal_selector).modal();
                });
            });
}



function myClearForm($form) {
    $form.find('.form-group').removeClass('has-error');
    $form.find('.help-block .ajax_field_error').remove();
    $form.find('#ajax_non_field_errors').remove();
    $form.find('#ajax_form_success').remove();
}

function myScrollPage(selector, step) {
    if ($(selector).length)
        $('html, body').animate({scrollTop: $(selector).offset().top - step}, 'fast');
    return false;
}


function myShowInfoInAlert($form, data) {
    var html = '<div id="ajax_form_success" class="alert alert-success">' +
        '<button type="button" class="close" data-dismiss="alert" aria-hidden="true">&times;</button>';
    if (data['response_header']) html += '<h4>' + data['response_header'] + '</h4>';
    html += data['response_body'] +
        '</div>';
    $form.prepend(html);
}


function myDisplayNonfieldError($form, error) {
    var html = '<div id="ajax_non_field_errors" class="alert alert-danger">' +
        '<button type="button" class="close" data-dismiss="alert" aria-hidden="true">&times;</button>' +
        error +
        '</div>';
//    var find1 = $form.find('.form-actions:last');
    var find2 = $form.find('.form-group:last');
//    if (find1.length)
//        find1.before(html);
    if (find2.length)
        find2.before(html);

}

function myDisplayFormErrors($form, errors) {
    for (var k in errors) if (errors.hasOwnProperty(k)) {
        $form.find(':input[name=' + k + ']').closest(".form-group").addClass('has-error');
        $form.find(':input[name=' + k + ']').closest(".form-group").find('.help-block').prepend('<li class="ajax_field_error">' + errors[k] + '</li>');
        if (k === 'captcha') {
            $form.find('input[name=captcha_1]').closest(".form-group").addClass('has-error');
            $form.find('input[name=captcha_1]').closest(".form-group").find('.help-block').prepend('<li class="ajax_field_error">' + errors[k] + '</li>');
        }
        if (k === 'non_field') {
            myDisplayNonfieldError($form, errors[k]);
        }
    }
}

function myUpdateValues(values) {
    for (var key in values) if (values.hasOwnProperty(key)) {
        if ($.trim(values[key]) === 'None')
            $('#' + key).text('');
        else
        {
            $('#' + key).text(values[key]);
            $('#' + key).val(values[key]);
        }
    }
}

function myUpdCaptcha($form, data) {
    if (data["captcha_key"] && data["captcha_image"]) {
        $form.find("img.captcha").attr('src', data["captcha_image"]);
        $form.find('#id_captcha_0').val(data["captcha_key"]);
        $form.find('#id_captcha_1').val('');
    }
}

function mySubmitAjaxForm(form_element, type, results_element, hide_elements) {
    var $form = $(form_element);
    var $args_length = arguments.length;
    $form.submit(function (event) {
        event.preventDefault();
        $.ajax({ // create an AJAX call...
            data: $form.serialize(), // get the form data
            type: $form.attr('method'), // GET or POST
            url: $form.attr('action'), // the file to call
            dataType: 'json',
            timeout: 60000,
            beforeSend: function (jqXHR, settings) {
                $form.find('input, select').attr('disabled', true); // запрещаем редактировать инпуты
                if ($args_length < 4 || hide_elements) {
                    $form.closest('div').css("visibility", "hidden");
                    $('footer').css("visibility", 'hidden');
                }
                myClearForm($form);
            },
            error: function (jqXHR, textStatus, errorThrown) {
                myDisplayNonfieldError($form, "ERROR: " + errorThrown);
            },
            success: function (data, textStatus, jqXHR) {
                myUpdCaptcha($form, data);
                if (data["result"] === 'success') {
                    myUpdateValues(data["update_values"]);
                    if ($args_length >= 2 && type === 'datas') {
//                        myShowDatasInModal(data);
                        if ($args_length >= 3)
                            $(results_element).html(data['response_body']);
                    }
                    else {
                        myShowInfoInAlert($form, data);
                        myScrollPage("#ajax_form_success", 55);
                    }
                }
                else if (data["result"] === 'error') {
                    myDisplayFormErrors($form, data["errors"]);
                }
            },
            complete: function (jqXHR, textStatus) {
                if ($args_length < 4 || hide_elements) {
                     $('footer').css("visibility", 'visible');
                     $form.closest('div').css("visibility", "visible");
                }

                $form.find('input, select').removeAttr('disabled'); // разрешаем редактировать инпуты
            }
        });
    });
}


function myRefreshCaptcha(captcha_url, caption) {
    $("img.captcha").css({"margin-bottom": 5, "width": 100, "height": 30});
    $("img.captcha").after('<a class="js-captcha-refresh" style="display: inline-block; margin-left: 10px; cursor: pointer"><i class="glyphicon glyphicon-refresh"></i> ' +
        caption + '</a>');
    $('.js-captcha-refresh').click(function (e) {
        e.preventDefault();
        var $form = $(this).closest('form');
        $.getJSON(captcha_url, function (data) {
            $form.find("img.captcha").attr('src', data['image_url']);
            $form.find('#id_captcha_0').val(data['key']);
            $form.find('#id_captcha_1').val('');
        });
    });
}

