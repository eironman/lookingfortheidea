$(document).on('ready', function() {
    $('.reply-trigger').on('click', function() {

        // Prepare the reply form
        var commentId = $(this).data('comment-id');
        var commentForm =
            $('.form').clone()
                .removeClass('mt50')
                .addClass('mt10');

        // Remove legend tag
        $(commentForm).find('legend').remove();

        // Update the parent id
        $(commentForm).find('input[name="comment_parent"]').val(commentId);

        // Append the form
        $(this).parent('.reply-action').after(commentForm);

        $(this).hide();
    });
});