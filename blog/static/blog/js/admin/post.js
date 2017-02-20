var $ = django.jQuery;
$(document).on('ready', function()
{
    // Button to send the notification about a new post to subscribers
    if (!$("#id_notification_sent").is(':checked')) {
        var sendNotificationTrigger =
            '<input style="margin-left: 20px" type="button" value="Send to subscribers" id="subscribers_send">'
        $('label[for="id_notification_sent"]').after(sendNotificationTrigger);
        $('#subscribers_send').on('click', function() {
            if (confirm('Are you sure?')) {
                sendPostNotification();
            }
        });
    }
});

// Sends the notification about a new post to subscribers
function sendPostNotification()
{
    // Set the security token
    var csrftoken = Helper.getCookie('csrftoken')
    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });

    $.ajax({
        method: "POST",
        url: '/blog/send_post_subscription',
        data: {
            post_id: $("#id_postmedia_set-0-post").val()
        }
    })
    .done(function(response) {
        if (response.status == 'ok') {
            $("#id_notification_sent").attr('checked','checked');
            $('input[name="_continue"]').trigger('click');
        } else {
            alert(response.msg);
        }
    })
    .error(function() {
        alert('An error occurred sending the notifications');
    });
}