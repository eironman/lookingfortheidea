from django.shortcuts import get_object_or_404, render
from django.conf import settings
from django.http import HttpResponseRedirect
from django.urls import reverse
from ratelimit.decorators import ratelimit
from bs4 import BeautifulSoup
from .models import Post, PostComment


def posts_list(request):
    """Post list"""
    post_list = Post.objects.order_by('-pub_date')
    context = {'post_list': post_list}
    return render(request, 'blog/posts_list.html', context)


def content(request, post_url):
    """Post content"""
    post = get_object_or_404(Post, url=post_url)
    post_list = Post.objects.values('url', 'title', 'pub_date').order_by('-pub_date')
    context = {
        'post': post,
        'comments': post.postcomment_set.all(),
        'post_media': post.postmedia_set.all(),
        'post_list': post_list,
        'load_jquery': settings.BLOG_LOAD_JQUERY
    }
    return render(request, 'blog/content.html', context)


@ratelimit(key='ip', rate='4/h', block=True)
def comment(request, post_url):
    """User comments a post"""
    post = get_object_or_404(Post, url=post_url)
    comment_author = request.POST['comment_author']
    comment_content = request.POST['comment_content']

    # All fields are mandatory
    if not comment_author or not comment_content:
        context = {
            'post': post,
            'comment_author': comment_author,
            'comment_content': comment_content,
            'error_message': "Completa todos los campos por favor"
        }
        return render(request, 'blog/content.html', context)

    # HTML tags are not allowed
    author_has_html_tags = \
        bool(BeautifulSoup(comment_author, "html.parser").find())
    content_has_html_tags =\
        bool(BeautifulSoup(comment_content, "html.parser").find())
    if author_has_html_tags or content_has_html_tags:
        context = {
            'post': post,
            'comment_author': comment_author,
            'comment_content': comment_content,
            'error_message': "Etiquetas HTML no están permitidas"
        }
        return render(request, 'blog/content.html', context)

    # Save comment
    comment = PostComment(post=post, owner=comment_author, content=comment_content)
    comment.save()

    return HttpResponseRedirect(reverse('blog:content', args=(post_url,)))