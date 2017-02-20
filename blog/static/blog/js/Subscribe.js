var Subscribe = {

    phone: null,
    email: null,

    disableSaveButton: function()
    {
        $('#trigger_subscribe').val('').addClass('loading').attr('disabled', 'disabled');
    },

    enableSaveButton: function()
    {
        $('#trigger_subscribe').val('¡SÍ, QUIERO!').removeClass('loading').removeAttr('disabled');
    },

    hideSubscribeModal: function()
    {
        $('.opacity_layer, .subscribe_form_modal').hide();
        $('.opacity_layer, .close_subscribe').off('click', Subscribe.hideSubscribeModal);
        Subscribe.resetSubscribeModal();
    },

    hideSubscribeButton: function()
    {
        $('#show_subscribe').hide();
    },

    removeMessages: function()
    {
        $('.subscribe_error_message').html('');
        $('.subscribe_info_message').html('');
        $('input[name="subscribe_phone"], input[name="subscribe_email"]').removeClass('error');
    },

    resetSubscribeModal: function()
    {
        $('input[name="subscribe_phone"], input[name="subscribe_email"]').val('');
        this.phone = '';
        this.email = '';
        this.removeMessages();


        $("#trigger_subscribe").show();
        $('input[name="subscribe_phone"]').show();
        $('input[name="subscribe_email"]').show();
        $('#and_or').show();
        $('select[name=country_code]').show();
        $("#subscribe_form legend").show();
    },

    saveSubscriber: function()
    {
        var self = this;
        this.disableSaveButton();

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
          url: $("#subscribe_form").attr('action'),
          data: {
            phone: this.phone,
            email: this.email
           }
        })
        .done(function(response) {
            if (response.status == 'ok') {
                self.storeSubscriberLocally();
                self.showSuccessModal();
                self.hideSubscribeButton();
                Unsubscribe.showUnsubscribeButton();
            } else {
                self.showError(response.msg);
            }
            self.enableSaveButton();
        })
        .error(function() {
            self.showError('¡Vaya! Ha ocurrido un error al suscribirte (2).');
            self.enableSaveButton();
        });
    },

    showError: function(msg)
    {
        $('.subscribe_error_message').html(msg);
    },

    showInfo: function(msg)
    {
        $('.subscribe_info_message').html(msg);
    },

    showSubscribeButton: function()
    {
        $('#show_subscribe').show();
    },

    showSubscribeModal: function()
    {
        $('.opacity_layer, .subscribe_form_modal').show();
        $('.opacity_layer, .close_subscribe').on('click', Subscribe.hideSubscribeModal);
    },

    showSuccessModal: function()
    {
        this.showInfo('¡Hecho! Muchas gracias, ya puedes recibir notificaciones :)');
        $("#trigger_subscribe").hide();
        $('input[name="subscribe_phone"]').hide();
        $('input[name="subscribe_email"]').hide();
        $('#and_or').hide();
        $('select[name=country_code]').hide();
        $("#subscribe_form legend").hide();
    },

    // Stores subscriber data into local storage
    storeSubscriberLocally: function()
    {
        Storage.set('bli_subscriber_email', this.email);
        Storage.set('bli_subscriber_phone', this.phone);
    },

    // Check if the data of a subscriber is valid
    validateSubscriberData: function()
    {
        this.phone = $('input[name="subscribe_phone"]').val().replace(/ /g, '');
        this.email = $('input[name="subscribe_email"]').val().replace(/ /g, '');

        // Security checks
        if (Helper.isEmpty(this.phone) && Helper.isEmpty(this.email)) {
            $('input[name="subscribe_phone"], input[name="subscribe_email"]').addClass('error');
            this.showError('¡Hey! Debes completar como mínimo uno de los campos');
            return false;
        }
        if (!Helper.isEmpty(this.email) && !Helper.validateEmail(this.email)) {
            $('input[name="subscribe_email"]').addClass('error');
            $('input[name="subscribe_phone"]').removeClass('error');
            this.showError('¡Ups! El email no es válido');
            return false;
        }
        if (!Helper.isEmpty(this.phone)) {
            if (!this.phone.match(/^\d+$/)) {
                $('input[name="subscribe_phone"]').addClass('error');
                $('input[name="subscribe_email"]').removeClass('error');
                this.showError('¡Ups! El teléfono no es válido');
                return false;
            }
            this.phone = '+' + $('select[name=country_code]').val() + this.phone;
        }

        this.removeMessages();

        return true;
    },

    init: function()
    {
        // Show subscribe button?
        this.email = Storage.get('bli_subscriber_email');
        this.phone = Storage.get('bli_subscriber_phone');
        if (Helper.isEmpty(this.email) && Helper.isEmpty(this.phone)) {
            this.showSubscribeButton();
        }

        // Show modal
        $('#show_subscribe').on('click', this.showSubscribeModal);

        // User clicks on subscribe
        var self = this;
        $('#trigger_subscribe').on('click', function() {
            if (self.validateSubscriberData()) {
                self.saveSubscriber();
            }
        });
    }
};
