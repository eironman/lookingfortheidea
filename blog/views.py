from django.conf import settings
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from ratelimit.decorators import ratelimit
from buscandolaidea.helper import has_forbidden_content
from .email import BlogMailer
from .models import Post, PostComment, Subscriber


def cancel_subscription(request):
    return render(request, 'blog/cancel_subscription.html')


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
@ratelimit(key='ip', rate='3/h', block=True)
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
    if has_forbidden_content(comment_author) or has_forbidden_content(comment_content):
        context = {
            'post': post,
            'comments': post.postcomment_set.all(),
            'comment_author': comment_author,
            'comment_content': comment_content,
            'error_message': "Contenido no permitido"
        }
        return render(request, 'blog/content.html', context)

    # Save comment
    comment_object = PostComment(post=post, owner=comment_author, content=comment_content, parent_id=comment_parent)
    comment_object.save()

    # Send comment
    blog_email = BlogMailer(request)
    blog_email.new_comment(comment_content, comment_author, post_url, post.title)

    return HttpResponseRedirect(reverse('blog:post_content', args=[post_url]))


def posts_list(request):
    """Post list"""
    post_list = Post.objects.order_by('-pub_date')
    context = {'post_list': post_list}
    return render(request, 'blog/posts_list.html', context)


def send_post_subscription(request):
    """Sends the notification about a new post to subscribers"""
    post_id = request.POST.get('post_id')

    if post_id:
        try:
            post = Post.objects.get(id=post_id)
            if post:
                # Send notification
                emails = list(Subscriber.objects.values_list('email', flat=True).exclude(email=''))
                blog_email = BlogMailer(request)
                blog_email.new_post(post.url, post.title, emails)

                # TODO: Send whatsapp messages
                # phones = list(Subscriber.objects.values_list('phone', flat=True).exclude(phone=''))

                return JsonResponse({'status': 'ok'})

        except Subscriber.DoesNotExist:
            return JsonResponse({'status': 'ko', 'msg': 'Post does not exist'})
    else:
        return JsonResponse({'status': 'ko', 'msg': 'No post id provided'})


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

        # Send welcome email
        if email:
            blog_email = BlogMailer(request)
            blog_email.new_subscriber(email)

        return JsonResponse({'status': 'ok'})
    else:
        return JsonResponse({'status': 'ko', 'msg': '¡Vaya! Hubo un error al crear la suscripción (1).'})


def unsubscribe(request):
    """Remove a subscriber"""
    email = request.POST.get('email')
    phone = request.POST.get('phone')
    exists = False

    if email:
        try:
            subscriber = Subscriber.objects.get(email=email)
            subscriber.delete()
            exists = True
        except Subscriber.DoesNotExist:
            None

    if phone:
        try:
            subscriber = Subscriber.objects.get(phone=phone)
            subscriber.delete()
            exists = True
        except Subscriber.DoesNotExist:
            None

    if exists:
        return JsonResponse({'status': 'ok'})
    else:
        return JsonResponse({'status': 'ko', 'msg': '¡Vaya! No hay nadie registrado con estos datos'})
