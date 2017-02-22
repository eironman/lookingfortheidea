var Comment = {

	// Security checks before sending comment
    validateCommentForm: function(form)
    {
        var commentAuthor = form.find('input[name="comment_author"]').val();
        var commentContent = form.find('textarea').val();
        if (commentAuthor == '' || commentContent == '') {
            // Remove previous error message
            form.find('.text-color-a').remove();

            // Show error message
            var errorMessage = '<p class="mb10 text-color-a">Completa todos los campos por favor</p>';
            form.find('input[type="hidden"]').first().before(errorMessage);
            return false;
        }
    },

    // Creates the reply form for a comment
    appendReplyForm: function(replyButton)
    {
        // Prepare the reply form
        var commentId = replyButton.data('comment-id');
        var replyForm =
            $('.comment_form.mt50').clone()
                .removeClass('mt50')
                .addClass('mt10');

        // Remove error message
        $(replyForm).find('.text-color-a').remove();

        // Remove legend tag
        $(replyForm).find('legend').remove();

        // Update the parent id
        $(replyForm).find('input[name="comment_parent"]').val(commentId);

        // Append the form
        replyButton.parent('.reply-action').after(replyForm);

        replyButton.hide();
    },

    init: function()
    {
        var self = this;

        // Check mandatory fields for comment
        $('.container').on('submit', '.comment_form', function() {
            return self.validateCommentForm($(this));
        });

        // Show reply comment form
        $('.reply-trigger').on('click', function() {
            self.appendReplyForm($(this));
        });
    }
};