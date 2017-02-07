from django.shortcuts import render
from django.core.mail import EmailMessage
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
    else:

        # Store message
        contact_message = ContactMessage(
            name=name,
            email=user_email,
            message=message_content
        )
        contact_message.save()

        # Send message
        recipients = ['info@buscandolaidea.com']
        if user_email:
            recipients.append(user_email)

        email = EmailMessage(
            '[Buscando La Idea] Mensaje de ' + name,
            message_content,
            'info@buscandolaidea.com',
            recipients,
            reply_to=['info@buscandolaidea.com']
        )
        email.send()

        context = {
            'success_message': "¡Muchas gracias por tu mensaje!"
        }

    return render(request, 'contact/contact.html', context)