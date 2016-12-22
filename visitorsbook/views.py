from django.shortcuts import render
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import VisitorBookMessage


def visitorsbook(request):
    """Visitors page"""
    signatures = VisitorBookMessage.objects.all()
    return render(request, 'visitorsbook/visitorsbook.html', {'signatures': signatures})


def publish(request):
    """Visitor publishes message"""
    name = request.POST['name']
    message = request.POST['message']
    image = None
    if 'visitor_image' in request.FILES:
        image = request.FILES['visitor_image']

    if not name or not message:
        context = {
            'name': name,
            'message': message,
            'error_message': "¡Ups! Necesitamos tu nombre y tu mensaje por favor"
        }
        return render(request, 'visitorsbook/visitorsbook.html', context)
    else:

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
