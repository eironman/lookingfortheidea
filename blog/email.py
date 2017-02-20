from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string


class BlogEmail:
    """Sends the emails for the blog: comments, new subscribers, new posts"""

    msg_plain = None
    msg_html = None
    email_to = None
    subject = None
    email_bcc = None

    def new_comment(self, comment_content, author, post_url, post_title):
        self.msg_plain =\
            render_to_string('email/new_comment_plain.txt', {'content': comment_content, 'blog_post_url': post_url})
        self.msg_html = \
            render_to_string('email/new_comment_html.html',
                             {'content': comment_content, 'blog_post_url': post_url, 'title': post_title})

        self.email_to = 'info@buscandolaidea.com'
        self.subject = 'Comentario de ' + author
        self.__send_email()

    def new_post(self, post_url, post_title, emails):
        self.msg_plain = render_to_string('email/new_post_plain.txt', {'blog_post_url': post_url})
        self.msg_html = render_to_string('email/new_post_html.html', {'blog_post_url': post_url, 'title': post_title})
        self.email_to = 'info@buscandolaidea.com'
        self.email_bcc = emails
        self.subject = post_title
        self.__send_email()

    def new_subscriber(self, subscriber_email):
        self.msg_plain = render_to_string('email/new_subscriber_plain.txt')
        self.msg_html = render_to_string('email/new_subscriber_html.html')
        self.email_to = subscriber_email
        self.subject = 'Suscripción confirmada'
        self.__send_email()

    def __send_email(self):
        email = EmailMultiAlternatives(
            '[Buscando La Idea] ' + self.subject,
            self.msg_plain,
            'info@buscandolaidea.com',
            [self.email_to]
        )

        if self.email_bcc:
            email.bcc = self.email_bcc

        if self.msg_html:
            email.attach_alternative(self.msg_html, 'text/html')

        email.send()
