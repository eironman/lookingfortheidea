from django.test import TestCase
from django.urls import reverse
from .models import Post


def create_post(title, content):
    return Post.objects.create(title=title, content=content)


# Test index view
class IndexTest(TestCase):
    def test_index_view_with_no_posts(self):
        response = self.client.get(reverse('blog:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No posts are available.")
        self.assertQuerysetEqual(response.context['post_list'], [])

    def test_index_with_one_post(self):
        create_post('title', 'content')
        response = self.client.get(reverse('blog:index'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['post_list']), 1)


# Test content view
class ContentTest(TestCase):
    def test_content_view_with_no_existing_post(self):
        response = self.client.get(reverse('blog:content', args=(999,)))
        self.assertEqual(response.status_code, 404)
