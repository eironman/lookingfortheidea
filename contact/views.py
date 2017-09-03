from django.shortcuts import render
from django.core.mail import EmailMessage
from buscandolaidea.helper import has_forbidden_content
from .models import ContactMessage


def contact(request):
    """Contact page"""
    return render(request, 'contact/contact.html')


def message(request):
    """Contact message"""
    name = request.POST['name']
    user_email = request.POST['email']
    message_content = request.POST['message']

    if not name or not message_content:
        context = {
            'name': name,
            'email': user_email,
            'message': message_content,
            'error_message': "¡Ups! ¿Podrías decirme tu nombre y el mensaje por favor?"
        }
    elif has_forbidden_content(name) or has_forbidden_content(message_content):
        context = {
            'name': name,
            'email': user_email,
            'message': message_content,
            'error_message': "¡Ups! Contenido no permitido"
        }
    else:

        # Store message
        contact_message = ContactMessage(
            name=name,
            email=user_email,
            message=message_content
        )
        contact_message.save()

        # Send message to me
        email = EmailMessage(
            '[Buscando La Idea] Mensaje de ' + name,
            message_content,
            'info@buscandolaidea.com',
            ['info@buscandolaidea.com'],
            reply_to=['info@buscandolaidea.com']
        )
        email.send()

        # Send message to user
        if user_email:
            email = EmailMessage(
                '[Buscando La Idea] Mensaje de ' + name,
                message_content,
                'info@buscandolaidea.com',
                [user_email],
                reply_to=['info@buscandolaidea.com']
            )
            email.send()

        context = {
            'success_message': "¡Muchas gracias por tu mensaje!"
        }

    return render(request, 'contact/contact.html', context)