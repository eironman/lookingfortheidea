from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.urls import reverse


class BlogEmail:
    """Sends the emails for the blog: comments, new subscribers, new posts"""

    msg_plain = None
    msg_html = None
    email_to = None
    subject = None
    email_bcc = None

    def new_comment(self, request, comment_content, author, post_url, post_title):
        """Sends an email when there is a new comment"""
        url = self.__build_blog_post_url(request, post_url)
        self.msg_plain =\
            render_to_string('email/new_comment_plain.txt', {'content': comment_content, 'blog_post_url': url})
        self.msg_html = \
            render_to_string('email/new_comment_html.html',
                             {'content': comment_content, 'blog_post_url': url, 'title': post_title})

        self.email_to = 'info@buscandolaidea.com'
        self.subject = 'Comentario de ' + author
        self.__send_email()

    def new_post(self, request, post_url, post_title, emails):
        """Sends the email for a new post"""
        self.subject = post_title
        blog_post_url = self.__build_blog_post_url(request, post_url)
        for email in emails:
            unsubscribe_url = self.__build_unsubscribe_url(request, email)
            self.msg_plain = \
                render_to_string(
                    'email/new_post_plain.txt',
                    {'blog_post_url': blog_post_url, 'unsubscribe_url': unsubscribe_url}
                )
            self.msg_html = \
                render_to_string(
                    'email/new_post_html.html',
                    {'blog_post_url': blog_post_url, 'title': post_title, 'unsubscribe_url': unsubscribe_url}
                )
            self.email_to = email
            self.__send_email()

    def new_subscriber(self, request, subscriber_email):
        """Sends the welcome email for a new subscriber"""
        unsubscribe_url = self.__build_unsubscribe_url(request, subscriber_email)
        self.msg_plain = render_to_string('email/new_subscriber_plain.txt', {'unsubscribe_url': unsubscribe_url})
        self.msg_html = render_to_string('email/new_subscriber_html.html', {'unsubscribe_url': unsubscribe_url})
        self.email_to = subscriber_email
        self.subject = 'Suscripción confirmada'
        self.__send_email()

    @staticmethod
    def __build_blog_post_url(request, post_url):
        location = reverse('blog:post_content', args=[post_url])
        return request.build_absolute_uri(location)

    @staticmethod
    def __build_unsubscribe_url(request, email):
        location = reverse('blog:cancel_subscription')
        url = request.build_absolute_uri(location) + "?e=" + email
        return url

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
