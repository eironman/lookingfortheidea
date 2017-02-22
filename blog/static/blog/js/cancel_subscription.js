$(document).on('ready', function()
{
    showUnsubscribeModalButton = false;
    Unsubscribe.init(showUnsubscribeModalButton);
    Unsubscribe.hideCancelButton();
    Unsubscribe.populateSubscriberInfo();
});