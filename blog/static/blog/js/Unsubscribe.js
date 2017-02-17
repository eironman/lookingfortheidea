var Unsubscribe = {

    phone: null,
    email: null,

    disableConfirmButton: function()
    {
        $('#trigger_unsubscribe').val('').addClass('loading').attr('disabled', 'disabled');
    },

    enableConfirmButton: function()
    {
        $('#trigger_unsubscribe').val('¡ESTOY SEGURO!').removeClass('loading').removeAttr('disabled');
    },

    hideUnsubscribeButton: function()
    {
        $('#show_unsubscribe').hide();
    },

    hideUnsubscribeModal: function()
    {
        $('.opacity_layer, .unsubscribe_form_modal').hide();
        Unsubscribe.resetUnsuscribeModal();
        $('.opacity_layer, .close_unsubscribe').off('click', Unsubscribe.hideUnsubscribeModal);
    },

    removeMessages: function()
    {
        $('.unsubscribe_error_message').html('');
        $('.unsubscribe_info_message').html('');
    },

    removeSubscriber: function()
    {
        var self = this;
        this.disableConfirmButton();
        this.email = Storage.get('bli_subscriber_email');
        this.phone = Storage.get('bli_subscriber_phone');

        // Set the security token
        var csrftoken = Helper.getCookie('csrftoken')
        $.ajaxSetup({
            beforeSend: function(xhr, settings) {
                if (!this.crossDomain) {
                    xhr.setRequestHeader("X-CSRFToken", csrftoken);
                }
            }
        });

        // Save
        $.ajax({
          method: "POST",
          url: $("#unsubscribe_form").attr('action'),
          data: {
            csrfmiddlewaretoken: $('input[name="csrfmiddlewaretoken"]').val(),
            phone: this.phone,
            email: this.email
           }
        })
        .done(function(response) {
            if (response.status == 'ok') {
                self.showSuccessModal();
                self.removeSubscriberLocally();
                self.hideUnsubscribeButton();
                Subscribe.showSubscribeButton();
            } else {
                self.showError('¡Vaya! Ha ocurrido un error al desuscribirte (1).');
            }
            self.enableConfirmButton();
        })
        .error(function() {
            self.showError('¡Vaya! Ha ocurrido un error al desuscribirte (2).');
            self.enableConfirmButton();
        });
    },

    // Removes subscriber data from local storage
    removeSubscriberLocally: function()
    {
        Storage.remove('bli_subscriber_email');
        Storage.remove('bli_subscriber_phone');
    },

    resetUnsuscribeModal: function()
    {
        $("#trigger_unsubscribe").show();
        $("#unsubscribe_form legend").show();
        $(".close_unsubscribe").val('MEJOR NO');
        this.removeMessages();
    },

    showError: function(msg)
    {
        $('.unsubscribe_error_message').html(msg);
    },

    showInfo: function(msg)
    {
        $('.unsubscribe_info_message').html(msg);
    },

    showSuccessModal: function() {
        this.showInfo('Hecho, espero que estés contento...');
        $("#trigger_unsubscribe").hide();
        $("#unsubscribe_form legend").hide();
        $(".close_unsubscribe").val('CERRAR');
    },

    showUnsubscribeButton: function()
    {
        $('#show_unsubscribe').show();
    },

    showUnsubscribeModal: function()
    {
        $('.opacity_layer, .unsubscribe_form_modal').show();
        $('.opacity_layer, .close_unsubscribe').on('click', Unsubscribe.hideUnsubscribeModal);
    },

    init: function() {
        this.email = Storage.get('bli_subscriber_email');
        this.phone = Storage.get('bli_subscriber_phone');
        if (!Helper.isEmpty(this.email) || !Helper.isEmpty(this.phone)) {
            this.showUnsubscribeButton();
        } else {
            this.hideUnsubscribeButton();
        }

        // Show modal
        $('#show_unsubscribe').on('click', this.showUnsubscribeModal);

        // User clicks on unsubscribe
        var self = this;
        $('#trigger_unsubscribe').on('click', function() {
            self.removeSubscriber()
        });
    }
};
