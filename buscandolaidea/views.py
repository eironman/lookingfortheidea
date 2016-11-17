from django.shortcuts import render
from blog.models import Post


# Homepage
def home(request):
    post_list = Post.objects.order_by('-pub_date')
    context = {'post_list': post_list}
    return render(request, 'buscandolaidea/base_template.html', context)
