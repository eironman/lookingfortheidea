from django.shortcuts import render
from django.core.mail import send_mail
from .models import ContactMessage


def contact(request):
    """Contact page"""
    return render(request, 'contact/contact.html')


def message(request):
    """Contact message"""
    name = request.POST['name']
    email = request.POST['email']
    message = request.POST['message']

    if not name or not message:
        context = {
            'name': name,
            'email': email,
            'message': message,
            'error_message': "¡Ups! ¿Podrías decirme tu nombre y el mensaje por favor?"
        }
    else:

        # Store message
        contact_message = ContactMessage(
            name=name,
            email=email,
            message=message
        )
        contact_message.sa

        # Send message
        send_mail(
            '[Buscando La Idea] Mensaje de ' + name,
            'Correo: %s\n\nMensaje:\n%s' % (email, message),
            'aaron.amengual@gmail.com',
            ['aaron.amengual@gmail.com'],
            fail_silently=False,
        )
        context = {
            'success_message': "¡Muchas gracias por tu mensaje!"
        }

    return render(request, 'contact/contact.html', context)