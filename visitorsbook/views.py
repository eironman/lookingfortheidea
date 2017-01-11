from django.shortcuts import render
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.urls import reverse
from bs4 import BeautifulSoup
from .models import VisitorBookMessage


def visitorsbook(request):
    """Visitors page"""
    signatures = VisitorBookMessage.objects.all()
    return render(request, 'visitorsbook/visitorsbook.html', {'signatures': signatures})


def publish(request):
    """Visitor publishes message"""

    # 20 MB
    max_upload_size = 20971520
    allowed_content_types = ['image/jpeg', 'image/png']
    image = None
    error_message = None
    name = request.POST['name']
    message = request.POST['message']

    # Name and message are mandatory
    if not name or not message:
        error_message = "¡Ups! Necesitamos tu nombre y tu mensaje por favor"

    # Image
    if 'visitor_image' in request.FILES:
        image = request.FILES['visitor_image']
        content_type = image.content_type
        if content_type not in allowed_content_types:
            error_message = "Tipo de archivo no permitido"
        elif image._size > max_upload_size:
            error_message = "Imagen demasiado grande"

    # HTML tags are not allowed
    name_has_html_tags = \
        bool(BeautifulSoup(name, "html.parser").find())
    message_has_html_tags = \
        bool(BeautifulSoup(message, "html.parser").find())
    if name_has_html_tags or message_has_html_tags:
        error_message = "Etiquetas HTML no están permitidas"

    # Exit if error
    if error_message:
        context = {
            'name': name,
            'message': message,
            'error_message': error_message
        }
        return render(request, 'visitorsbook/visitorsbook.html', context)

    # Store message
    contact_message = VisitorBookMessage(
        name=name,
        message=message,
        image=image
    )
    contact_message.save()

    # Send email
    send_mail(
        '[Buscando La Idea] Mensaje en el libro de visitas',
        'Nombre:\n%s\n\nMensaje:\n%s' % (name, message),
        'info@buscandolaidea.com',
        ['aaron.amengual@gmail.com'],
        fail_silently=True
    )

    return HttpResponseRedirect(reverse('visitorsbook:visitorsbook'), {'success_message': '¡Muchas gracias por tu firma!'})
