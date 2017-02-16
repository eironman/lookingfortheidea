function validateEmail(email) {
    var re = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
    return re.test(email);
}

$(document).on('ready', function() {

    // Show subscribe modal
    $('#show_subscribe').on('click', function() {
        $('.opacity_layer, .modal').show();
    });

    // Hide subscribe modal
    $('.opacity_layer, .close_subscribe').on('click', function() {
        $('.opacity_layer, .modal').hide();
    });

    // Add subscriber
    $('#trigger_subscribe').on('click', function() {
        var phone = $('input[name="subscribe_phone"]').val().replace(/ /g, '');
        var country = $('select[name=country_code]').val();
        var email = $('input[name="subscribe_email"]').val().replace(/ /g, '');
        var csrf = $('input[name="csrfmiddlewaretoken"]').val();

        // Security checks
        if (phone == '' && email == '') {
            $('input[name="subscribe_phone"], input[name="subscribe_email"]').addClass('error');
            $('.subscribe_error_message').html('Debes completar como mínimo uno de los campos');
            return;
        }
        if (email != '' && !validateEmail(email)) {
            $('input[name="subscribe_email"]').addClass('error');
            $('input[name="subscribe_phone"]').removeClass('error');
            $('.subscribe_error_message').html('El email no es válido');
            return;
        }
        if (phone != '' && !phone.match(/^\d+$/)) {
            $('input[name="subscribe_phone"]').addClass('error');
            $('input[name="subscribe_email"]').removeClass('error');
            $('.subscribe_error_message').html('El teléfono no es válido');
            return;
        }

        // Remove messages
        $('.subscribe_error_message').html('');
        $('.subscribe_info_message').html('');
        $('input[name="subscribe_phone"], input[name="subscribe_email"]').removeClass('error');

        // Disable save button
        $(this).val('').addClass('loading').attr('disabled', 'disabled');

        // Save
        $.ajax({
          method: "POST",
          url: $("#subscribe_form").attr('action'),
          data: {
            csrfmiddlewaretoken: csrf,
            phone: phone,
            country: country,
            email: email
           }
        })
        .done(function(response) {
            if (response.status == 'ok') {
                $('.subscribe_info_message').html('¡Hecho! Muchas gracias, ya puedes recibir notificaciones :)');
                $('input[name="subscribe_phone"]').val('');
                $('input[name="subscribe_email"]').val('');
                // TODO: STORE SUBSCRIPTION INFO INTO LOCAL STORAGE
            } else {
                $('.subscribe_error_message').html(response.msg);
            }
            $('#trigger_subscribe').val('¡SÍ, QUIERO!').removeClass('loading').removeAttr('disabled');
        })
        .error(function() {
            $('.subscribe_error_message').html('¡Vaya! Ha ocurrido un error al suscribirte (2).');
            $('#trigger_subscribe').val('¡SÍ, QUIERO!').removeClass('loading').removeAttr('disabled');
        });
    });
});