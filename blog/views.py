from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.template.loader import render_to_string
from django.urls import reverse
from ratelimit.decorators import ratelimit
from bs4 import BeautifulSoup
from .models import Post, PostComment, Subscriber


def content(request, post_url):
    """Post content"""
    post = get_object_or_404(Post, url=post_url)
    post_list = Post.objects.filter(publish=True).values('url', 'title', 'pub_date').order_by('-pub_date')
    context = {
        'post': post,
        'comments': post.postcomment_set.filter(parent_id=None),
        'post_media': post.postmedia_set.all(),
        'post_list': post_list,
        'load_jquery': settings.BLOG_LOAD_JQUERY
    }
    return render(request, 'blog/content.html', context)


# Raise forbidden if an ip makes more than 4 comments per hour
@ratelimit(key='ip', rate='4/h', block=True)
def comment(request, post_url):
    """User comments a post"""
    post = get_object_or_404(Post, url=post_url)
    comment_author = request.POST['comment_author']
    comment_content = request.POST['comment_content']
    comment_parent = request.POST['comment_parent']

    # Mandatory fields
    if not comment_author or not comment_content:
        context = {
            'post': post,
            'comments': post.postcomment_set.all(),
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
            'comments': post.postcomment_set.all(),
            'comment_author': comment_author,
            'comment_content': comment_content,
            'error_message': "Etiquetas HTML no están permitidas"
        }
        return render(request, 'blog/content.html', context)

    # Save comment
    comment_object = PostComment(post=post, owner=comment_author, content=comment_content, parent_id=comment_parent)
    comment_object.save()

    # Send comment

    # Build post url
    location = reverse('blog:post_content', args=[post_url])
    url = request.build_absolute_uri(location)

    # Build email content
    msg_plain = render_to_string('email/plain.txt', {'content': comment_content, 'blog_post_url': url})
    msg_html =\
        render_to_string('email/html.html', {'content': comment_content, 'blog_post_url': url, 'title': post.title})

    # Send it
    email = EmailMultiAlternatives(
        '[Buscando La Idea] Comentario de ' + comment_author,
        msg_plain,
        'info@buscandolaidea.com',
        ['info@buscandolaidea.com']
    )
    email.attach_alternative(msg_html, 'text/html')
    email.send()

    return HttpResponseRedirect(reverse('blog:post_content', args=[post_url]))


def posts_list(request):
    """Post list"""
    post_list = Post.objects.order_by('-pub_date')
    context = {'post_list': post_list}
    return render(request, 'blog/posts_list.html', context)


def subscribe(request):
    """Add a subscriber"""
    email = request.POST.get('email')
    phone = request.POST.get('phone')

    # Check if email or phone are already registered
    if email:
        try:
            subscriber = Subscriber.objects.get(email=email)
            if subscriber.email:
                return JsonResponse({'status': 'ko', 'msg': '¡Vaya! Esta dirección de correo ya está suscrita.'})
        except Subscriber.DoesNotExist:
            None

    if phone:
        try:
            subscriber = Subscriber.objects.get(phone=phone)
            if subscriber.phone:
                return JsonResponse({'status': 'ko', 'msg': '¡Vaya! Este teléfono ya está suscrito.'})
        except Subscriber.DoesNotExist:
            None

    # Create subscriber
    subscriber_object = Subscriber(email=email, phone=phone)
    subscriber_object.save()
    if subscriber_object.id:
        return JsonResponse({'status': 'ok'})
    else:
        return JsonResponse({'status': 'ko', 'msg': '¡Vaya! Hubo un error al crear la suscripción (1).'})

def unsubscribe(request):
    """Remove a subscriber"""
    email = request.POST.get('email')
    phone = request.POST.get('phone')

    if email:
        try:
            subscriber = Subscriber.objects.get(email=email)
            subscriber.delete()
        except Subscriber.DoesNotExist:
            None

    if phone:
        try:
            subscriber = Subscriber.objects.get(phone=phone)
            subscriber.delete()
        except Subscriber.DoesNotExist:
            None

    return JsonResponse({'status': 'ok'})
