$(document).on('ready', function() {

    // Show reply form
    $('.reply-trigger').on('click', function() {
        console.log('append');
        // Prepare the reply form
        var commentId = $(this).data('comment-id');
        var replyForm =
            $('.form.mt50').clone()
                .removeClass('mt50')
                .addClass('mt10');

        // Remove error message
        $(replyForm).find('.text-color-a').remove();

        // Remove legend tag
        $(replyForm).find('legend').remove();

        // Update the parent id
        $(replyForm).find('input[name="comment_parent"]').val(commentId);

        // Append the form
        $(this).parent('.reply-action').after(replyForm);

        $(this).hide();
    });

    // Check mandatory fields
    $('.container').on('submit', '.form', function() {
        var commentAuthor = $(this).find('input[name="comment_author"]').val();
        var commentContent = $(this).find('textarea').val();
        if (commentAuthor == '' || commentContent == '') {
            // Remove previous error message
            $(this).find('.text-color-a').remove();

            // Show error message
            var errorMessage = '<p class="mb10 text-color-a">Completa todos los campos por favor</p>';
            $(this).find('input[type="hidden"]').first().before(errorMessage);
            return false;
        }
    });
});