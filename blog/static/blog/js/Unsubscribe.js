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

    getSubscriberData: function()
    {
        var emailParam = Helper.getUrlParameter('e');
        if (!Helper.isEmpty(emailParam)) {
            this.email = emailParam;
        } else {
            this.email = Storage.get('bli_subscriber_email');
        }
        // this.phone = Storage.get('bli_subscriber_phone');
    },

    hideCancelButton: function()
    {
        $(".close_unsubscribe").hide();
    },

    hideUnsubscribeButton: function()
    {
        $('#show_unsubscribe').hide();
    },

    hideUnsubscribeModal: function()
    {
        $('.opacity_layer, .unsubscribe_form_modal').hide();
        $('.opacity_layer, .close_unsubscribe').off('click', Unsubscribe.hideUnsubscribeModal);
        Unsubscribe.resetUnsuscribeModal();
    },

    populateSubscriberInfo: function()
    {
        this.getSubscriberData();
        var subscriberInfo = 'Estás suscrito como: ' + this.email;
        /* if (!Helper.isEmpty(this.email)) {
            subscriberInfo += '<br><br>' + this.email;
        }
        if (!Helper.isEmpty(this.phone)) {
            subscriberInfo += '<br><br>' + this.phone;
        } */
        this.showInfo(subscriberInfo);
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
        this.getSubscriberData();

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
                if (typeof Subscribe !== 'undefined') {
                    Subscribe.showSubscribeButton();
                }
            } else {
                self.showError(response.msg);
            }
            self.enableConfirmButton();
        })
        .error(function() {
            self.showError('¡Vaya! Ha ocurrido un error al desuscribirte.');
            self.enableConfirmButton();
        });
    },

    // Removes subscriber data from local storage
    removeSubscriberLocally: function()
    {
        // Check if the user unsuscribes from the cancel_unsubscribe page
        // which means that maybe the email is different than the one stored locally
        var localEmail = Storage.get('bli_subscriber_email');
        if (localEmail === this.email) {
            Storage.remove('bli_subscriber_email');
        }
        var localPhone = Storage.get('bli_subscriber_phone');
        if (localPhone === this.phone) {
            Storage.remove('bli_subscriber_phone');
        }
    },

    resetUnsuscribeModal: function()
    {
        $("#trigger_unsubscribe").show();
        $("#unsubscribe_form legend").show();
        $(".close_unsubscribe").val('MEJOR NO');
        this.phone = '';
        this.email = '';
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
        $('.opacity_layer, .close_unsubscribe').on('click', this.hideUnsubscribeModal);
    },

    init: function(toggleUnsubscribeButton)
    {
        var self = this;

        // Show/hide unsubscribe button
        if (toggleUnsubscribeButton !== false) {
            // Show unsubscribe button?
            this.getSubscriberData();
            if (!Helper.isEmpty(this.email) || !Helper.isEmpty(this.phone)) {
                this.showUnsubscribeButton();
            }

            // Show modal
            $('#show_unsubscribe').on('click', function() {
                self.populateSubscriberInfo();
                self.showUnsubscribeModal();
            });
        }

        // User clicks on unsubscribe
        $('#trigger_unsubscribe').on('click', function() {
            self.removeSubscriber()
        });
    }
};
