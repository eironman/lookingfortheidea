from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Post, PostComment


# Post list
def posts_list(request):
    post_list = Post.objects.order_by('-pub_date')
    context = {'post_list': post_list}
    return render(request, 'blog/posts_list.html', context)


# Post content
def content(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    context = {
        'post': post,
        'comments': post.postcomment_set.order_by('-pub_date')
    }
    return render(request, 'blog/content.html', context)


# User comments a post
def comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    author = request.POST['author']
    comment_content = request.POST['content']
    # All fields are mandatory
    if not author or not comment_content:
        context = {
            'post': post,
            'author': author,
            'comment_content': comment_content,
            'error_message': "Completa todos los campos por favor"
        }
        return render(request, 'blog/content.html', context)

    # Save comment
    comment = PostComment(post=post, owner=author, content=comment_content)
    comment.save()

    return HttpResponseRedirect(reverse('blog:content', args=(post_id,)))